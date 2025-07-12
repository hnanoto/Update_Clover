import subprocess
import sys
import os
import shutil
import hashlib
from config import SCRIPT_DIR, RED, GREEN, YELLOW, MIN_CLOVER_ZIP_SIZE, CLOVER_SHA256
from logger import logger
from config import GREEN, RED

class CloverUpdateError(Exception):
    """Exceção personalizada para erros relacionados à atualização do Clover."""
    pass

def run_command(command):
    """Executa um comando no terminal e retorna o código de saída, stdout e stderr."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr

def check_environment():
    """Verifica se o ambiente é macOS."""
    logger("verifying_environment", YELLOW)
    if sys.platform != "darwin":
        raise CloverUpdateError("error_environment")
    logger("environment_verified", GREEN)

def check_dependencies():
    """Verifica se as dependências necessárias estão instaladas."""
    logger("verifying_dependencies", YELLOW)
    dependencies = ["curl", "unzip", "/usr/libexec/PlistBuddy", "installer"]
    for dep in dependencies:
        ret_code, _, _ = run_command(["which", dep])
        if ret_code != 0:
            raise CloverUpdateError(f"error_dependency_not_found", dep=dep)
    logger("all_dependencies_available", GREEN)

def validate_clover_zip(file_path):
    """Verifica se o arquivo Clover.zip é válido."""
    if not os.path.exists(file_path):
        raise CloverUpdateError(f"error_clover_zip_small", file_path=file_path)

    if os.path.getsize(file_path) < MIN_CLOVER_ZIP_SIZE:
        raise CloverUpdateError("error_clover_zip_small")

    ret_code, _, _ = run_command(["unzip", "-t", file_path])
    if ret_code != 0:
        raise CloverUpdateError("error_invalid_zip")

    if CLOVER_SHA256:
        logger("verifying_file_integrity", YELLOW)
        sha256_hash = hashlib.sha256()
        with open(file_path,"rb") as f:
            # Lê o arquivo em pedaços para evitar sobrecarga de memória
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
        if sha256_hash.hexdigest() != CLOVER_SHA256:
            raise CloverUpdateError("error_verifying_integrity")
        logger("file_integrity_verified", GREEN)

def cleanup():
    """Limpa arquivos temporários."""
    logger("cleaning_up", YELLOW)
    try:
        os.remove(f"{SCRIPT_DIR}/Clover.zip")
    except FileNotFoundError:
        logger("file_not_found", YELLOW, file_path=f"{SCRIPT_DIR}/Clover.zip")
    except Exception as e:
        logger("error_removing_file", RED, file_path=f"{SCRIPT_DIR}/Clover.zip", error=e)

    try:
        shutil.rmtree(f"{SCRIPT_DIR}/Clover_extracted")
    except FileNotFoundError:
        logger("directory_not_found", YELLOW, dir_path=f"{SCRIPT_DIR}/Clover_extracted")
    except Exception as e:
        logger("error_removing_directory", RED, dir_path=f"{SCRIPT_DIR}/Clover_extracted", error=e)

    logger("cleanup_completed", GREEN)

def download_ocbinarydata():
    import subprocess
    import os
    from config import SCRIPT_DIR
    oc_dir = os.path.join(SCRIPT_DIR, 'OcBinaryData')
    if os.path.exists(oc_dir):
        logger('OcBinaryData já está presente.', GREEN)
        return oc_dir
    try:
        logger('Clonando OcBinaryData...', GREEN)
        subprocess.run(['git', 'clone', '--depth=1', 'https://github.com/acidanthera/OcBinaryData.git', oc_dir], check=True)
        logger('OcBinaryData clonado com sucesso.', GREEN)
        return oc_dir
    except subprocess.CalledProcessError:
        logger('Erro ao clonar o repositório OcBinaryData.', RED)
        raise CloverUpdateError('Falha ao clonar OcBinaryData.')


def copy_hfsplus_driver(ocbinarydata_dir, target_drivers_dir):
    import shutil
    import os
    source = os.path.join(ocbinarydata_dir, 'Drivers', 'HFSPlus.efi')
    if not os.path.isfile(source):
        logger('driver_not_found', RED)
        return
    os.makedirs(target_drivers_dir, exist_ok=True)
    destination = os.path.join(target_drivers_dir, 'HFSPlus.efi')
    shutil.copy2(source, destination)
    logger('hfsplus_driver_copied', GREEN)
