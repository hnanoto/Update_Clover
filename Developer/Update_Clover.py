#!/usr/bin/env python3

import subprocess
import os
import sys
import time
import shutil
import datetime
import glob

# Cores para feedback visual
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
NC = "\033[0;m"  # Sem cor

# Caminho absoluto para o diretório do script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Arquivo de log com timestamp
LOGFILE = f"update_clover_{time.strftime('%Y%m%d%H%M%S')}.log"

# --- VARIÁVEL PARA O DIRETÓRIO DE BACKUP ---
# Escolha um local com espaço suficiente, por exemplo, a pasta do usuário.
# Será criada uma pasta 'EFI_BACKUPS' dentro do diretório escolhido
BACKUP_BASE_DIR = os.path.expanduser("~")

# Declaração da variável EFI_DIR com escopo global (para o script)
EFI_DIR = ""

def logger(message, color=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color_prefix = color if color else ""
    color_suffix = NC if color else ""
    log_message = f"[{timestamp}] {color_prefix}{message}{color_suffix}"
    print(log_message)
    with open(LOGFILE, "a") as log_file:
        log_file.write(log_message + "\n")

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr

def check_environment():
    logger("Verificando ambiente...", YELLOW)
    if sys.platform != "darwin":
        logger("Erro: Este script deve ser executado no macOS.", RED)
        sys.exit(1)
    logger("Ambiente verificado com sucesso.", GREEN)

def check_dependencies():
    logger("Verificando dependências...", YELLOW)
    dependencies = ["curl", "unzip", "/usr/libexec/PlistBuddy", "installer"]
    for dep in dependencies:
        ret_code, _, _ = run_command(["which", dep])
        if ret_code != 0:
            logger(f"Erro: Dependência '{dep}' não encontrada.", RED)
            sys.exit(1)
    logger("Todas as dependências estão disponíveis.", GREEN)

def download_clover():
    logger("Baixando a última versão do Clover do seu repositório...", YELLOW)

    # Obtém a última release do seu fork
    ret_code, stdout, stderr = run_command([
        "curl", "-s",
        "https://api.github.com/repos/hnanoto/CloverBootloader-Hackintosh-and-Beyond/releases/latest"
    ])
    if ret_code != 0:
        logger("Erro ao obter informações da última release do Clover.", RED)
        sys.exit(1)

    try:
        import json
        release_info = json.loads(stdout)
        assets = release_info.get('assets', [])
        for asset in assets:
            if "Clover" in asset.get('name', '') and asset.get('name', '').endswith(".zip"):
                clover_latest_release_url = asset.get('browser_download_url')
                break
        else:
            clover_latest_release_url = None
    except ImportError:
        logger("Erro: Módulo 'json' não encontrado. Tentando método alternativo...", RED)
        import re
        match = re.search(r'"browser_download_url":\s*"(https://github\.com/.*?Clover.*?.zip)"', stdout)
        clover_latest_release_url = match.group(1) if match else None

    if not clover_latest_release_url:
        logger("Erro: Não foi possível obter o link da última versão do Clover.", RED)
        sys.exit(1)

    # Baixar o arquivo Clover.zip
    logger(f"Link de download do Clover encontrado: {clover_latest_release_url}", GREEN)
    ret_code, _, stderr = run_command(["curl", "-L", "-o", f"{SCRIPT_DIR}/Clover.zip", clover_latest_release_url])
    if ret_code != 0:
        logger("Erro: O download do Clover falhou.", RED)
        sys.exit(1)

    # Verificar o tamanho do arquivo
    clover_zip_size = os.path.getsize(f"{SCRIPT_DIR}/Clover.zip")
    if clover_zip_size < 1000000:
        logger("Erro: O arquivo Clover.zip baixado está muito pequeno. Provavelmente o download falhou.", RED)
        os.remove(f"{SCRIPT_DIR}/Clover.zip")
        sys.exit(1)

    # Verificar se o arquivo é um ZIP válido
    ret_code, _, _ = run_command(["unzip", "-t", f"{SCRIPT_DIR}/Clover.zip"])
    if ret_code != 0:
        logger("Erro: O arquivo Clover.zip baixado não é um arquivo ZIP válido.", RED)
        os.remove(f"{SCRIPT_DIR}/Clover.zip")
        sys.exit(1)

    logger("Clover baixado com sucesso.", GREEN)

def list_all_efi():
    global EFI_DIR
    logger("Localizando todas as partições EFI no sistema...", YELLOW)
    ret_code, stdout, stderr = run_command(["diskutil", "list"])
    if ret_code != 0:
        logger("Erro ao listar partições.", RED)
        sys.exit(1)

    efi_partitions = [line.split()[-1] for line in stdout.splitlines() if "EFI" in line]
    if not efi_partitions:
        logger("Erro: Nenhuma partição EFI encontrada.", RED)
        sys.exit(1)

    logger("Partições EFI detectadas:")
    for idx, part in enumerate(efi_partitions):
        print(f"{idx + 1}. {part}")
    print(f"{len(efi_partitions) + 1}. Sair")

    while True:
        try:
            choice = int(input(
                f"Selecione o número da partição EFI que deseja usar (ou {len(efi_partitions) + 1} para sair): "))
            if choice == len(efi_partitions) + 1:
                logger("Saindo do script...", YELLOW)
                sys.exit(0)
            elif 1 <= choice <= len(efi_partitions):
                selected_efi = efi_partitions[choice - 1]
                ret_code, stdout, stderr = run_command(["diskutil", "info", selected_efi])
                if ret_code == 0:
                    mount_point_line = [line for line in stdout.splitlines() if "Mount Point" in line]
                    if mount_point_line:
                        EFI_DIR = mount_point_line[0].split(':', 1)[1].strip()
                        if not EFI_DIR:
                            logger(f"Erro: A partição EFI selecionada não está montada.", RED)
                            logger(
                                f"Monte a EFI manualmente usando: 'diskutil mount {selected_efi}' e execute o script novamente.",
                                YELLOW)
                            sys.exit(1)
                        logger(f"Partição EFI selecionada: {selected_efi}")
                        logger(f"Ponto de montagem: {EFI_DIR}")
                        break
                    else:
                        logger(f"Erro: Não foi possível encontrar o ponto de montagem para {selected_efi}", RED)
                        sys.exit(1)
                else:
                    logger(f"Erro ao obter informações para {selected_efi}", RED)
                    sys.exit(1)
            else:
                logger("Seleção inválida. Tente novamente.", RED)
        except ValueError:
            logger("Por favor, insira um número válido.", RED)

def backup_efi():
    backup_base_dir = os.path.join(BACKUP_BASE_DIR, "EFI_BACKUPS")
    timestamp = time.strftime('%Y%m%d%H%M%S')
    backup_dir = os.path.join(backup_base_dir, f"EFI-Backup-{timestamp}")

    # Verifica se o diretório já existe e adiciona um sufixo numérico, se necessário
    count = 1
    while os.path.exists(backup_dir):
        backup_dir = os.path.join(backup_base_dir, f"EFI-Backup-{timestamp}-{count}")
        count += 1

    logger(f"Criando backup em {backup_dir}...", YELLOW)

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

        logger(f"Backup criado com sucesso em '{backup_dir}'.", GREEN)

    except Exception as e:
        logger(f"Erro ao criar o backup: {e}", RED)
        sys.exit(1)

def update_clover_files():
    logger("Atualizando arquivos do Clover...", YELLOW)
    clover_extracted_dir = os.path.join(SCRIPT_DIR, "Clover_extracted")
    logger("Descompactando o Clover...", YELLOW)
    ret_code, _, stderr = run_command(["unzip", "-o", f"{SCRIPT_DIR}/Clover.zip", "-d", clover_extracted_dir])
    if ret_code != 0:
        logger("Erro ao descompactar o Clover.", RED)
        sys.exit(1)

    if not os.path.isdir(clover_extracted_dir):
        logger("Erro: Diretório 'Clover_extracted' não foi criado.", RED)
        sys.exit(1)

    logger("Copiando os arquivos do Clover para a EFI...", YELLOW)
    clover_efi_dir = os.path.join(clover_extracted_dir, "CloverV2", "EFI")

    logger("Atualizando BOOTX64.efi...", YELLOW)
    shutil.copy(f"{clover_efi_dir}/BOOT/BOOTX64.efi", f"{EFI_DIR}/EFI/BOOT/BOOTX64.efi")

    logger("Atualizando CLOVERX64.efi...", YELLOW)
    shutil.copy(f"{clover_efi_dir}/CLOVER/CLOVERX64.efi", f"{EFI_DIR}/EFI/CLOVER/CLOVERX64.efi")

    if any(ret_code != 0 for ret_code, _, _ in [
        run_command(["ls", f"{EFI_DIR}/EFI/BOOT/BOOTX64.efi"]),
        run_command(["ls", f"{EFI_DIR}/EFI/CLOVER/CLOVERX64.efi"])
    ]):
        logger("Erro ao copiar os arquivos do Clover para a EFI.", RED)
        sys.exit(1)

    logger("Arquivos do Clover atualizados com sucesso.", GREEN)

def update_clover_drivers():
    logger("Atualizando drivers UEFI do Clover...", YELLOW)
    clover_drivers_dir = os.path.join(SCRIPT_DIR, "Clover_extracted", "CloverV2", "EFI", "CLOVER", "Drivers")
    efi_drivers_dir = os.path.join(EFI_DIR, "EFI", "CLOVER", "Drivers")
    efi_uefi_dir = os.path.join(efi_drivers_dir, "UEFI")
    clover_uefi_off_dir = os.path.join(clover_drivers_dir, "Off", "UEFI")

    if not os.path.isdir(efi_uefi_dir):
        logger(f"Erro: A pasta UEFI não foi encontrada em {efi_drivers_dir}.", RED)
        sys.exit(1)

    # Subpastas dentro de Off/UEFI onde os drivers estão localizados
    clover_driver_subfolders = ["FileSystem", "FileVault2", "HID", "MemoryFix", "Other"]

    logger(f"Listando drivers em {efi_uefi_dir}...", YELLOW)

    # Lista os drivers existentes na pasta UEFI da EFI principal
    existing_drivers = glob.glob(os.path.join(efi_uefi_dir, "*.efi"))

    for driver_path in existing_drivers:
        driver_basename = os.path.basename(driver_path)
        driver_updated = False # Flag para verificar se o driver foi atualizado

        # Verifica se o driver existe em alguma das subpastas do Clover baixado
        for subfolder in clover_driver_subfolders:
            clover_driver_path = os.path.join(clover_uefi_off_dir, subfolder, driver_basename)
            if os.path.isfile(clover_driver_path):
                logger(f"Atualizando driver: {driver_basename}...", YELLOW)
                try:
                    shutil.copy2(clover_driver_path, driver_path)  # Copia, preservando metadados
                    logger(f"Driver {driver_basename} atualizado.", GREEN)
                    driver_updated = True
                    break  # Sai do loop interno se o driver for atualizado
                except Exception as e:
                    logger(f"Erro ao atualizar o driver {driver_basename}: {e}", RED)
                    sys.exit(1)
        
        if not driver_updated:
            logger(f"Driver {driver_basename} não encontrado no Clover baixado ou não atualizado. Ignorando...", YELLOW)

    logger("Drivers UEFI do Clover atualizados.", GREEN)

def cleanup():
    logger("Limpando arquivos temporários...", YELLOW)
    try:
        os.remove(f"{SCRIPT_DIR}/Clover.zip")
    except FileNotFoundError:
        logger(f"Arquivo '{SCRIPT_DIR}/Clover.zip' não encontrado. Ignorando...", YELLOW)
    except Exception as e:
        logger(f"Erro ao remover '{SCRIPT_DIR}/Clover.zip': {e}", RED)

    try:
        shutil.rmtree(f"{SCRIPT_DIR}/Clover_extracted")
    except FileNotFoundError:
        logger(f"Diretório '{SCRIPT_DIR}/Clover_extracted' não encontrado. Ignorando...", YELLOW)
    except Exception as e:
        logger(f"Erro ao remover '{SCRIPT_DIR}/Clover_extracted': {e}", RED)

    logger("Limpeza concluída.", GREEN)

if __name__ == "__main__":
    check_environment()
    check_dependencies()
    download_clover()
    list_all_efi()
    backup_efi()
    update_clover_files()
    update_clover_drivers()
    logger("Atualização do Clover concluída com sucesso!", GREEN)
    cleanup()