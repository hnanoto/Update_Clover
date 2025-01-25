#!/usr/bin/env python3

import os
from config import LOGFILE, SCRIPT_DIR
from utils import check_environment, check_dependencies, cleanup, CloverUpdateError
from efi_handler import list_all_efi, backup_efi
from clover_updater import download_clover
from logger import logger, GREEN, load_translations
from menu import exibir_menu

def main():
    """Função principal do script."""
    try:
        # Carrega as traduções do idioma do sistema ou usa inglês como padrão
        load_translations("")

        check_environment()
        check_dependencies()

        # Baixa o Clover apenas uma vez e obtém o caminho do arquivo
        clover_zip_path = os.path.join(SCRIPT_DIR, "Clover.zip")
        download_clover(clover_zip_path)

        efi_dir = list_all_efi()  # Obtenha o valor de EFI_DIR retornado por list_all_efi

        # Se EFI_DIR estiver definido, prossiga com o backup e o menu
        if efi_dir:
            backup_efi()
            exibir_menu(efi_dir, clover_zip_path)
            logger("update_successful", GREEN)  # Mensagem de sucesso
        else:
            logger("error_efi_dir_not_defined", RED)  # Mensagem de erro

    except SystemExit as se:
        if se.code != 0:
            logger("script_error", RED)
    except CloverUpdateError as e:
        logger("error", RED, error=e)  # Mensagem de erro formatada
    except Exception as e:
        logger("unexpected_error", RED, error=e)  # Mensagem de erro formatada
    finally:
        cleanup()
        logger("logs_saved", None, logfile=LOGFILE)  # Mensagem de log

if __name__ == "__main__":
    main()
