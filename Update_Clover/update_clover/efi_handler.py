import os
import time
import shutil
import sys
from config import BACKUP_BASE_DIR, YELLOW, RED, GREEN
from utils import run_command, CloverUpdateError
from logger import logger

# Declaração da variável EFI_DIR (será definida em list_all_efi)
EFI_DIR = ""

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
    global EFI_DIR
    logger("locating_efi_partitions", YELLOW)
    ret_code, stdout, stderr = run_command(["diskutil", "list"])
    if ret_code != 0:
        raise CloverUpdateError("error_list_partitions")

    efi_partitions = [line.split()[-1] for line in stdout.splitlines() if "EFI" in line]
    if not efi_partitions:
        raise CloverUpdateError("error_no_efi_partition")

    logger("efi_partitions_detected", YELLOW)
    for idx, part in enumerate(efi_partitions):
        print(f"{idx + 1}. {part}")
    print(f"{len(efi_partitions) + 1}. Exit")

    while True:
        choice_str = input(logger("choose_option", YELLOW))

        if not choice_str.isdigit():
            logger("invalid_input", RED)
            continue

        choice = int(choice_str)

        if choice == len(efi_partitions) + 1:
            logger("exiting", YELLOW)
            sys.exit(0)
        elif 1 <= choice <= len(efi_partitions):
            selected_efi = efi_partitions[choice - 1]
            logger("efi_partition_selected", GREEN, partition=selected_efi)

            # Loop para aguardar a montagem da partição, se necessário
            while True:
                ret_code, stdout, stderr = run_command(["diskutil", "info", selected_efi])
                if ret_code != 0:
                    raise CloverUpdateError("error_getting_efi_info", selected_efi=selected_efi)

                mount_point_line = [line for line in stdout.splitlines() if "Mount Point" in line]
                if mount_point_line:
                    EFI_DIR = mount_point_line[0].split(':', 1)[1].strip()
                    if EFI_DIR:
                        logger("mount_point", GREEN, mount_point=EFI_DIR)
                        break  # Sai do loop, pois a partição está montada
                    else:
                        logger("mount_wait", YELLOW, partition=selected_efi)
                        logger("press_ctrl_c_to_exit", YELLOW)
                        time.sleep(5)  # Aguarda 5 segundos antes de verificar novamente
                else:
                    logger("mount_error", YELLOW, partition=selected_efi)
                    time.sleep(5)  # Aguarda 5 segundos antes de verificar novamente

            # Neste ponto, a partição EFI está montada
            logger("efi_dir_after_mount", YELLOW, efi_dir=EFI_DIR)

            # Verifica se a EFI está montada como somente leitura e tenta remontá-la
            if is_efi_read_only(EFI_DIR):
                raise CloverUpdateError("read_only_error", mount_point=EFI_DIR)

            # Verifica qual é o gerenciador de boot
            bootloader = detect_bootloader(EFI_DIR)
            if bootloader == "Clover":
                logger("clover_detected", GREEN)
                return EFI_DIR  # Retorna o diretório EFI
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

def backup_efi():
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
        for item in os.listdir(EFI_DIR):
            s = os.path.join(EFI_DIR, item)
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


def update_clover_drivers(clover_extracted_dir, ocbinarydata_dir, efi_mount_point):
    import glob
    from utils import copy_hfsplus_driver
    logger('start_update_drivers', YELLOW)
    source_dir = os.path.join(clover_extracted_dir, 'EFI', 'CLOVER', 'drivers', 'UEFI')
    dest_dir = os.path.join(efi_mount_point, 'EFI', 'CLOVER', 'drivers', 'UEFI')
    logger('listing_drivers', YELLOW)
    if not os.path.isdir(source_dir):
        logger('driver_not_found', RED)
        return
    # Remove TODOS os arquivos antigos da pasta drivers/UEFI
    if os.path.isdir(dest_dir):
        for f in os.listdir(dest_dir):
            file_path = os.path.join(dest_dir, f)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass
    else:
        os.makedirs(dest_dir, exist_ok=True)
    # Copia todos os .efi novos
    for f in glob.glob(os.path.join(source_dir, '*.efi')):
        try:
            shutil.copy2(f, dest_dir)
            logger(f'Driver {os.path.basename(f)} atualizado', GREEN)
        except Exception:
            logger('driver_not_found', RED)
    # Copia HFSPlus.efi
    copy_hfsplus_driver(ocbinarydata_dir, dest_dir)
    logger('uefi_drivers_updated', GREEN)
