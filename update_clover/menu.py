from efi_handler import EFI_DIR, is_efi_read_only
from logger import logger, YELLOW, RED, GREEN
from clover_updater import (
    update_bootx64,
    update_cloverx64,
    update_clover_drivers,
)
import sys

def exibir_menu(efi_dir, clover_zip_path):
    """Exibe o menu principal e obtém a escolha do usuário."""
    while True:
        print("\nMenu de Atualização do Clover:")
        print("1. Atualizar BOOTX64.efi e CLOVERX64.efi")
        print("2. Atualizar Drivers")
        print("3. Atualização Completa")
        print("4. Sair")

        escolha = input("\nEscolha uma opção: ")

        # Verifica se a partição EFI está montada antes de prosseguir
        if not is_efi_read_only(efi_dir):
            logger(
                f"Partição EFI ({efi_dir}) está montada e pronta para atualização.",
                GREEN,
            )
        else:
            logger(
                f"Erro: A partição EFI ({efi_dir}) não está montada ou não está acessível para escrita. Monte-a antes de continuar.",
                RED,
            )
            continue

        if escolha == "1":
            atualizar_boot_clover(efi_dir, clover_zip_path)
        elif escolha == "2":
            atualizar_drivers(efi_dir, clover_zip_path)
        elif escolha == "3":
            atualizar_tudo(efi_dir, clover_zip_path)
        elif escolha == "4":
            logger("Saindo...", YELLOW)
            sys.exit(0)
        else:
            logger("Opção inválida. Por favor, escolha uma opção de 1 a 4.", RED)

def atualizar_bootx64(efi_dir, clover_zip_path):
    """Atualiza o arquivo BOOTX64.efi na partição EFI."""
    logger("Iniciando atualização do BOOTX64.efi...", YELLOW)
    try:
        update_bootx64(efi_dir, clover_zip_path)
        logger("BOOTX64.efi atualizado com sucesso!", GREEN)
    except Exception as e:
        logger(f"Erro ao atualizar BOOTX64.efi: {e}", RED)

def atualizar_cloverx64(efi_dir, clover_zip_path):
    """Atualiza o arquivo CLOVERX64.efi na partição EFI."""
    logger("Iniciando atualização do CLOVERX64.efi...", YELLOW)
    try:
        update_cloverx64(efi_dir, clover_zip_path)
        logger("CLOVERX64.efi atualizado com sucesso!", GREEN)
    except Exception as e:
        logger(f"Erro ao atualizar CLOVERX64.efi: {e}", RED)

def atualizar_drivers(efi_dir, clover_zip_path):
    """Atualiza os drivers UEFI na partição EFI."""
    logger("Iniciando atualização dos drivers UEFI...", YELLOW)
    try:
        update_clover_drivers(efi_dir, clover_zip_path)
        logger("Drivers UEFI atualizados com sucesso!", GREEN)
    except Exception as e:
        logger(f"Erro ao atualizar drivers UEFI: {e}", RED)

def atualizar_tudo(efi_dir, clover_zip_path):
    """Atualiza todos os componentes do Clover (BOOTX64.efi, CLOVERX64.efi e drivers)."""
    logger("Iniciando atualização completa do Clover...", YELLOW)
    try:
        atualizar_boot_clover(efi_dir, clover_zip_path)
        atualizar_drivers(efi_dir, clover_zip_path)
        logger("Atualização completa do Clover concluída com sucesso!", GREEN)
    except Exception as e:
        logger(f"Erro ao atualizar o Clover: {e}", RED)

def atualizar_boot_clover(efi_dir, clover_zip_path):
    """Atualiza os arquivos BOOTX64.efi e CLOVERX64.efi na partição EFI."""
    logger("Iniciando atualização do BOOTX64.efi e CLOVERX64.efi...", YELLOW)
    try:
        update_bootx64(efi_dir, clover_zip_path)
        update_cloverx64(efi_dir, clover_zip_path)
        logger("BOOTX64.efi e CLOVERX64.efi atualizados com sucesso!", GREEN)
    except Exception as e:
        logger(f"Erro ao atualizar BOOTX64.efi e CLOVERX64.efi: {e}", RED)