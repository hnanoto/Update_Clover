import os
import time
import shutil
import sys
from config import BACKUP_BASE_DIR, YELLOW, RED, GREEN
from utils import run_command, CloverUpdateError
from logger import logger

def is_efi_read_only(mount_point):
    """Verifica se a partição EFI está montada como somente leitura."""
    logger("checking_efi_read_only", YELLOW, mount_point=mount_point)
    ret_code, stdout, stderr = run_command(["mount"])
    if ret_code != 0:
        logger("error_getting_efi_info", RED, partition=mount_point)
        return True  # Assume que está como somente leitura em caso de erro

    for line in stdout.splitlines():
        if mount_point in line and "read-only" in line:
            logger("read_only_error", RED, mount_point=mount_point)
            return True
    logger("efi_read_write", GREEN, mount_point=mount_point)
    return False

def detect_bootloader(efi_dir):
    """Detecta qual gerenciador de boot está presente na partição EFI (Clover ou OpenCore)."""
    logger("detecting_bootloader", YELLOW, efi_dir=efi_dir)

    clover_path = os.path.join(efi_dir, "EFI", "CLOVER")
    opencore_path = os.path.join(efi_dir, "EFI", "OC")
    windows_bootmgr_path = os.path.join(efi_dir, "EFI", "Microsoft", "Boot", "bootmgfw.efi")

    if os.path.isdir(clover_path) and os.path.isfile(os.path.join(clover_path, "CLOVERX64.efi")):
        logger("clover_detected", GREEN)
        return "Clover"
    elif os.path.isdir(opencore_path) and os.path.isfile(os.path.join(opencore_path, "OpenCore.efi")):
        logger("opencore_detected", RED)
        return "OpenCore"
    elif os.path.isfile(windows_bootmgr_path):
        logger("windows_bootmgr_detected", YELLOW)
        return "Windows"
    else:
        logger("unknown_bootloader", YELLOW)
        return None

def list_all_efi():
    """Lista todas as partições EFI e permite ao usuário escolher uma."""
    logger("locating_efi_partitions", YELLOW)
    ret_code, stdout, stderr = run_command(["diskutil", "list"])
    if ret_code != 0:
        raise CloverUpdateError("error_list_partitions")

    efi_partitions = []
    # Permite varredura em pendrives FAT32 comuns além das partições fixas "EFI"
    allowed_types = ["EFI", "DOS_FAT_32", "Windows_FAT_32", "Microsoft Basic Data", "0xEF"]
    for line in stdout.splitlines():
        if any(t in line for t in allowed_types):
            parts = line.split()
            if len(parts) >= 4:
                candidate = parts[-1]
                # Verifica se o identificador segue a estrutura física de partição Apple (ej: disk2s1)
                if candidate.startswith("disk") and "s" in candidate:
                    size_unit = parts[-2]
                    size_val = parts[-3]
                    
                    # Limpa o número da partição (ex "1:" ou "*") no começo da linha
                    start_idx = 1 if (parts[0].endswith(":") or parts[0] == "*") else 0
                    
                    name_type_str = " ".join(parts[start_idx:-3])
                    
                    display_desc = f"{candidate} - {name_type_str} ({size_val} {size_unit})"
                    efi_partitions.append((candidate, display_desc))

    # Remover duplicatas mantendo a ordem através de dict nativo do Python 3.7+
    unique_partitions = {}
    for ident, desc in efi_partitions:
        if ident not in unique_partitions:
            unique_partitions[ident] = desc
    
    efi_partitions_list = list(unique_partitions.items())

    if not efi_partitions_list:
        raise CloverUpdateError("error_no_efi_partition")

    logger("efi_partitions_detected", YELLOW)
    for idx, (ident, desc) in enumerate(efi_partitions_list):
        print(f"{idx + 1}. {desc}")
    print(f"{len(efi_partitions_list) + 1}. Exit")

    while True:
        choice_str = input(logger("choose_option", YELLOW))

        if not choice_str.isdigit():
            logger("invalid_input", RED)
            continue

        choice = int(choice_str)

        if choice == len(efi_partitions_list) + 1:
            logger("exiting", YELLOW)
            sys.exit(0)
        elif 1 <= choice <= len(efi_partitions_list):
            selected_efi = efi_partitions_list[choice - 1][0]
            logger("efi_partition_selected", GREEN, partition=selected_efi)

            # Loop para aguardar a montagem da partição, se necessário
            while True:
                ret_code, stdout, stderr = run_command(["diskutil", "info", selected_efi])
                if ret_code != 0:
                    raise CloverUpdateError("error_getting_efi_info", selected_efi=selected_efi)

                mount_point_line = [line for line in stdout.splitlines() if "Mount Point" in line]
                if mount_point_line:
                    efi_dir_mounted = mount_point_line[0].split(':', 1)[1].strip()
                    if efi_dir_mounted:
                        logger("mount_point", GREEN, mount_point=efi_dir_mounted)
                        break  # Sai do loop, pois a partição está montada
                    else:
                        logger("mount_wait", YELLOW, partition=selected_efi)
                        logger("press_ctrl_c_to_exit", YELLOW)
                        time.sleep(5)  # Aguarda 5 segundos antes de verificar novamente
                else:
                    logger("mount_error", YELLOW, partition=selected_efi)
                    time.sleep(5)  # Aguarda 5 segundos antes de verificar novamente

            # Neste ponto, a partição EFI está montada
            logger("efi_dir_after_mount", YELLOW, efi_dir=efi_dir_mounted)

            # Verifica se a EFI está montada como somente leitura e tenta remontá-la
            if is_efi_read_only(efi_dir_mounted):
                raise CloverUpdateError("read_only_error", mount_point=efi_dir_mounted)

            # Verifica qual é o gerenciador de boot
            bootloader = detect_bootloader(efi_dir_mounted)
            if bootloader == "Clover":
                logger("clover_detected", GREEN)
                return efi_dir_mounted  # Retorna o diretório EFI
            elif bootloader == "OpenCore":
                logger("not_clover_abort", RED)
                sys.exit(1)
            elif bootloader == "Windows":
                logger("windows_bootmgr_detected", RED)
                sys.exit(1)
            else:
                logger("unknown_bootloader", RED)
                sys.exit(1)
        else:
            logger("invalid_choice", RED)

def backup_efi(efi_dir):
    """Cria um backup da partição EFI selecionada."""
    backup_base_dir = os.path.join(BACKUP_BASE_DIR, "EFI_BACKUPS")
    timestamp = time.strftime('%Y%m%d%H%M%S')
    backup_dir = os.path.join(backup_base_dir, f"EFI-Backup-{timestamp}")

    # Verifica se o diretório já existe e adiciona um sufixo numérico, se necessário
    count = 1
    while os.path.exists(backup_dir):
        backup_dir = os.path.join(backup_base_dir, f"EFI-Backup-{timestamp}-{count}")
        count += 1

    logger("creating_backup", YELLOW, backup_dir=backup_dir)

    os.makedirs(backup_dir, exist_ok=True)

    try:
        # Copia a estrutura de diretórios e arquivos.
        for item in os.listdir(efi_dir):
            s = os.path.join(efi_dir, item)
            d = os.path.join(backup_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks=False, ignore=None)
            else:
                shutil.copy2(s, d)

        # Corrige as permissões do diretório de backup
        for root, dirs, files in os.walk(backup_dir):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o755)  # Permissão de leitura e execução para todos
            for f in files:
                os.chmod(os.path.join(root, f), 0o644)  # Permissão de leitura para todos

        logger("backup_created", GREEN, backup_dir=backup_dir)

    except Exception as e:
        raise CloverUpdateError("error_creating_backup", error=e)


