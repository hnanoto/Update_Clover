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
    logger(f"Verificando se {mount_point} está montado como somente leitura...", YELLOW)
    ret_code, stdout, stderr = run_command(["mount"])
    if ret_code != 0:
        logger(f"Erro ao executar o comando 'mount': {stderr}", RED)
        return True  # Assume que está como somente leitura em caso de erro

    for line in stdout.splitlines():
        if mount_point in line and "read-only" in line:
            logger(f"{mount_point} está montado como somente leitura.", RED)
            return True
    logger(f"{mount_point} está montado como leitura/gravação.", GREEN)
    return False

def detect_bootloader(efi_dir):
    """Detecta qual gerenciador de boot está presente na partição EFI (Clover ou OpenCore)."""
    logger(f"Detectando gerenciador de boot em {efi_dir}...", YELLOW)

    clover_path = os.path.join(efi_dir, "EFI", "CLOVER")
    opencore_path = os.path.join(efi_dir, "EFI", "OC")
    windows_bootmgr_path = os.path.join(efi_dir, "EFI", "Microsoft", "Boot", "bootmgfw.efi")

    if os.path.isdir(clover_path) and os.path.isfile(os.path.join(clover_path, "CLOVERX64.efi")):
        logger("Clover detectado.", GREEN)
        return "Clover"
    elif os.path.isdir(opencore_path) and os.path.isfile(os.path.join(opencore_path, "OpenCore.efi")):
        logger("OpenCore detectado.", RED)
        return "OpenCore"
    elif os.path.isfile(windows_bootmgr_path):
        logger("Gerenciador de Boot do Windows detectado.", YELLOW)
        return "Windows"
    else:
        logger("Nenhum gerenciador de boot conhecido foi detectado.", YELLOW)
        return None

def list_all_efi():
    """Lista todas as partições EFI e permite ao usuário escolher uma."""
    global EFI_DIR
    logger("locating_efi_partitions", YELLOW)
    ret_code, stdout, stderr = run_command(["diskutil", "list"])
    if ret_code != 0:
        raise CloverUpdateError("Erro ao listar partições.")

    efi_partitions = [line.split()[-1] for line in stdout.splitlines() if "EFI" in line]
    if not efi_partitions:
        raise CloverUpdateError("Nenhuma partição EFI encontrada.")

    logger("efi_partitions_detected", YELLOW)
    for idx, part in enumerate(efi_partitions):
        print(f"{idx + 1}. {part}")
    print(f"{len(efi_partitions) + 1}. Sair")

    while True:
        choice_str = input(logger("select_efi_partition", YELLOW, total=len(efi_partitions)))

        if not choice_str.isdigit():
            logger("invalid_input", RED)
            continue

        choice = int(choice_str)

        if choice == len(efi_partitions) + 1:
            logger("exiting", YELLOW)
            sys.exit(0)
        elif 1 <= choice <= len(efi_partitions):
            selected_efi = efi_partitions[choice - 1]
            logger(f"Partição EFI selecionada: {selected_efi}", GREEN)

            # Loop para aguardar a montagem da partição, se necessário
            while True:
                ret_code, stdout, stderr = run_command(["diskutil", "info", selected_efi])
                if ret_code != 0:
                    raise CloverUpdateError(f"Erro ao obter informações para {selected_efi}")

                mount_point_line = [line for line in stdout.splitlines() if "Mount Point" in line]
                if mount_point_line:
                    EFI_DIR = mount_point_line[0].split(':', 1)[1].strip()
                    if EFI_DIR:
                        logger(f"Ponto de montagem: {EFI_DIR}", GREEN)
                        break  # Sai do loop, pois a partição está montada
                    else:
                        logger(f"A partição EFI {selected_efi} ainda não está montada. Aguardando...", YELLOW)
                        logger("Pressione Ctrl+C para interromper a espera e sair.", YELLOW)
                        time.sleep(5)  # Aguarda 5 segundos antes de verificar novamente
                else:
                    logger(f"Não foi possível encontrar o ponto de montagem para {selected_efi}. Aguardando...", YELLOW)
                    time.sleep(5)  # Aguarda 5 segundos antes de verificar novamente

            # Neste ponto, a partição EFI está montada
            logger(f"Valor de EFI_DIR após a montagem: {EFI_DIR}", YELLOW)

            # Verifica se a EFI está montada como somente leitura e tenta remontá-la
            if is_efi_read_only(EFI_DIR):
                raise CloverUpdateError(
                    "A partição EFI está montada como somente leitura. Monte-a com permissões de escrita e tente novamente."
                )

            # Verifica qual é o gerenciador de boot
            bootloader = detect_bootloader(EFI_DIR)
            if bootloader == "Clover":
                logger("Clover detectado na partição EFI. Continuando...", GREEN)
                return EFI_DIR  # Retorna o diretório EFI
            elif bootloader == "OpenCore":
                logger(
                    f"OpenCore detectado na partição EFI {EFI_DIR}. Este script é para atualizar o Clover. Abortando...",
                    RED,
                )
                sys.exit(1)
            elif bootloader == "Windows":
                logger(
                    f"Gerenciador de Boot do Windows detectado na partição EFI {EFI_DIR}. Este script é para atualizar o Clover. Abortando...",
                    RED,
                )
                sys.exit(1)
            else:
                logger(
                    f"Não foi possível determinar o gerenciador de boot na partição EFI {EFI_DIR}. Abortando...",
                    RED,
                )
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

    logger(f"creating_backup", YELLOW, backup_dir=backup_dir)

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

        logger(f"backup_created", GREEN, backup_dir=backup_dir)

    except Exception as e:
        raise CloverUpdateError(f"error_creating_backup {e}")