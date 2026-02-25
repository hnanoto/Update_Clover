import os
import shutil
import glob
import json
import re
import sys
from config import SCRIPT_DIR, CLOVER_OFFICIAL_REPO_URL, CLOVER_FORK_REPO_URL, YELLOW, RED, GREEN
from utils import run_command, CloverUpdateError, validate_clover_zip
from logger import logger

def download_clover(clover_zip_path):
    """Baixa a última versão do Clover do repositório."""
    logger("downloading_clover", YELLOW)

    # Verifica se uma URL de download direto foi fornecida
    if 'CLOVER_DOWNLOAD_URL' in os.environ:
        clover_latest_release_url = os.environ['CLOVER_DOWNLOAD_URL']
        logger("using_direct_download_url", GREEN, url=clover_latest_release_url)
    else:
        def fetch_url(api_url):
            ret_code, stdout, stderr = run_command(["curl", "-s", api_url])
            if ret_code != 0:
                return None
            try:
                release_info = json.loads(stdout)
                # Verifica se o Github negou a requisição (Rate limit Exceeded)
                if release_info.get("message") and "rate limit" in release_info.get("message", "").lower():
                    return None
                    
                assets = release_info.get('assets', [])
                for asset in assets:
                    if "Clover" in asset.get('name', '') and asset.get('name', '').endswith(".zip"):
                        return asset.get('browser_download_url')
            except Exception:
                # regex fallback
                match = re.search(r'"browser_download_url":\s*"(https://github\.com/.*?Clover.*?.zip)"', stdout)
                if match:
                    return match.group(1)
            return None

        # 1. Tenta o repositório oficial
        clover_latest_release_url = fetch_url(CLOVER_OFFICIAL_REPO_URL)
        if clover_latest_release_url:
            print(f"[{GREEN}✓\033[0;m] Repositório Fonte: CloverHackyColor (Oficial)")
        else:
            # 2. Em caso de falha API/Offline, parte para o Fork
            print(f"[{YELLOW}!\033[0;m] Serviço oficial instável. Tentando Fallback local (hnanoto)...")
            clover_latest_release_url = fetch_url(CLOVER_FORK_REPO_URL)

        if not clover_latest_release_url:
            raise CloverUpdateError("error_clover_link")

    # Baixar o arquivo Clover.zip
    logger("clover_download_link_found", GREEN, url=clover_latest_release_url)
    ret_code, _, stderr = run_command(["curl", "-L", "-o", clover_zip_path, clover_latest_release_url])
    if ret_code != 0:
        raise CloverUpdateError("error_download_failed")

    # Validar o arquivo baixado
    validate_clover_zip(clover_zip_path)

    logger("clover_downloaded", GREEN)

def update_bootx64(efi_dir, clover_extracted_dir):
    """Atualiza o arquivo BOOTX64.efi na partição EFI."""
    clover_efi_dir = os.path.join(clover_extracted_dir, "CloverV2", "EFI")

    # Cria os diretórios de destino se eles não existirem
    os.makedirs(os.path.join(efi_dir, "EFI/BOOT"), exist_ok=True)

    logger("updating_bootx64", YELLOW)
    try:
        shutil.copy(f"{clover_efi_dir}/BOOT/BOOTX64.efi", os.path.join(efi_dir, "EFI/BOOT/BOOTX64.efi"))
        logger("success_update_bootx64", GREEN)
    except Exception as e:
        raise CloverUpdateError(f"error_updating_bootx64 {e}")

def update_cloverx64(efi_dir, clover_extracted_dir):
    """Atualiza o arquivo CLOVERX64.efi na partição EFI."""
    clover_efi_dir = os.path.join(clover_extracted_dir, "CloverV2", "EFI")

    # Cria os diretórios de destino se eles não existirem
    os.makedirs(os.path.join(efi_dir, "EFI/CLOVER"), exist_ok=True)

    logger("updating_cloverx64", YELLOW)
    try:
        shutil.copy(f"{clover_efi_dir}/CLOVER/CLOVERX64.efi", os.path.join(efi_dir, "EFI/CLOVER/CLOVERX64.efi"))
        logger("success_update_cloverx64", GREEN)
    except Exception as e:
        raise CloverUpdateError(f"error_updating_cloverx64 {e}")

def update_clover_drivers(efi_dir, clover_extracted_dir, ocbinarydata_dir):
    """Atualiza os drivers UEFI do Clover na partição EFI."""
    logger("start_update_drivers", YELLOW)
    from utils import copy_hfsplus_driver
    
    clover_drivers_dir = os.path.join(clover_extracted_dir, "CloverV2", "EFI", "CLOVER", "Drivers")
    efi_drivers_dir = os.path.join(efi_dir, "EFI", "CLOVER", "Drivers")
    efi_uefi_dir = os.path.join(efi_drivers_dir, "UEFI")
    clover_uefi_off_dir = os.path.join(clover_drivers_dir, "Off", "UEFI")

    if not os.path.isdir(efi_uefi_dir):
        raise CloverUpdateError(f"error_uefi_folder_not_found {efi_drivers_dir}.")

    # Subpastas dentro de Off/UEFI onde os drivers estão localizados
    clover_driver_subfolders = ["FileSystem", "FileVault2", "HID", "MemoryFix", "Other"]

    logger("listing_drivers", YELLOW, efi_uefi_dir=efi_uefi_dir)

    # Lista os drivers existentes na pasta UEFI da EFI principal
    existing_drivers = glob.glob(os.path.join(efi_uefi_dir, "*.efi"))

    for driver_path in existing_drivers:
        driver_basename = os.path.basename(driver_path)
        if driver_basename.lower() == "hfsplus.efi":
            continue # HFSPlus is updated from OcBinaryData separately
            
        driver_updated = False  # Flag para verificar se o driver foi atualizado

        # Verifica se o driver existe em alguma das subpastas do Clover baixado
        for subfolder in clover_driver_subfolders:
            clover_driver_path = os.path.join(clover_uefi_off_dir, subfolder, driver_basename)
            if os.path.isfile(clover_driver_path):
                logger("updating_driver", YELLOW, driver_basename=driver_basename)
                try:
                    shutil.copy2(clover_driver_path, driver_path)  # Copia, preservando metadados
                    logger("driver_updated", GREEN, driver_basename=driver_basename)
                    driver_updated = True
                    break  # Sai do loop interno se o driver for atualizado
                except Exception as e:
                    raise CloverUpdateError(f"error_updating_driver {driver_basename} {e}")

        if not driver_updated:
            logger("driver_not_found", YELLOW, driver_basename=driver_basename)

    # Update HFSPlus.efi from OcBinaryData
    copy_hfsplus_driver(ocbinarydata_dir, efi_uefi_dir)

    logger("uefi_drivers_updated", GREEN)

def unzip_clover(clover_zip_path):
    """Descompacta o arquivo Clover.zip no diretório Clover_extracted."""
    clover_extracted_dir = os.path.join(SCRIPT_DIR, "Clover_extracted")
    logger("unpacking_clover", YELLOW)
    
    ret_code, _, stderr = run_command(["unzip", "-o", "-q", clover_zip_path, "-d", clover_extracted_dir])
    if ret_code != 0:
        raise CloverUpdateError("error_unpacking_clover")

    if not os.path.isdir(clover_extracted_dir):
        raise CloverUpdateError("error_directory_not_created")

    return clover_extracted_dir
