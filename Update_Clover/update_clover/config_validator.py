import os
import plistlib
import shutil
from logger import logger
from config import YELLOW, GREEN, RED
from utils import CloverUpdateError

def sync_plist_dicts(user_dict, sample_dict, log_path="Root"):
    """
    Recursiona sobre dicionários para adicionar Quirks faltantes (somente chaves novas)
    """
    changes_made = False
    if not isinstance(sample_dict, dict) or not isinstance(user_dict, dict):
        return False

    for key, value in sample_dict.items():
        if key not in user_dict:
            user_dict[key] = value
            # Notifica que adicionou uma Quirk faltante nova
            logger("added_missing_key", YELLOW, key=f"[{log_path} -> {key}]")
            changes_made = True
        elif isinstance(value, dict) and isinstance(user_dict[key], dict):
            # Recurcursão profunda só acontece entre dicionários
            if sync_plist_dicts(user_dict[key], value, log_path=f"{log_path}/{key}"):
                changes_made = True
    return changes_made

def check_config_plist(efi_dir, clover_extracted_dir):
    """
    Verifica e adiciona Quirks e Strings do Clover sample.plist no config.plist do usuario
    sem prejudicar/apagar a configuracao atual dele.
    """
    logger("start_config_update", YELLOW)

    user_config_path = os.path.join(efi_dir, "EFI", "CLOVER", "config.plist")
    sample_config_path = os.path.join(clover_extracted_dir, "CloverV2", "EFI", "CLOVER", "config-sample.plist")

    if not os.path.isfile(sample_config_path):
        raise CloverUpdateError(f"error_sample_plist_not_found {sample_config_path}")

    if not os.path.isfile(user_config_path):
        logger("config_plist_not_found", RED, path=user_config_path)
        return

    try:
        with open(sample_config_path, 'rb') as f:
            sample_plist = plistlib.load(f)

        with open(user_config_path, 'rb') as f:
            user_plist = plistlib.load(f)

        # Copia de Backup apenas de segurança antes de embutir os Quirks
        backup_path = user_config_path + ".bak"
        shutil.copy2(user_config_path, backup_path)
        logger("config_backup_created", GREEN, path=backup_path)

        # As seções do Clover que contém estrutura de Quirks baseada em OpenCore e UEFI.
        # Nós não faremos nas seções Device/ACPI para proteger os DSDTs e Patches do usuário.
        quirk_sections = ["Quirks", "BooterQuirks", "KernelQuirks", "UEFI"]
        
        changes = False
        
        for section in quirk_sections:
            if section in sample_plist:
                if section not in user_plist:
                    user_plist[section] = sample_plist[section]
                    logger("added_missing_key", YELLOW, key=f"Raiz/[{section}]")
                    changes = True
                else:
                    if sync_plist_dicts(user_plist[section], sample_plist[section], log_path=section):
                        changes = True
        
        if changes:
            with open(user_config_path, 'wb') as f:
                plistlib.dump(user_plist, f)
            logger("config_updated_successfully", GREEN)
        else:
            logger("config_already_up_to_date", GREEN)
            # Como nada de novo foi injetado (estava 100% Ok), removemos o backup
            os.remove(backup_path)

    except Exception as e:
        raise CloverUpdateError(f"error_updating_config {e}")
