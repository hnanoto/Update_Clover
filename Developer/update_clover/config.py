import os
import time

# Cores para feedback visual
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
NC = "\033[0;m"  # Sem cor

# Caminho absoluto para o diretório do script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Arquivo de log com timestamp
LOGFILE = os.path.join(SCRIPT_DIR, f"update_clover_{time.strftime('%Y%m%d%H%M%S')}.log")

# Diretório base para backups da EFI
BACKUP_BASE_DIR = os.path.expanduser("~")

# --- Configurações do Clover ---
# URL base do repositório do Clover (API do GitHub)
CLOVER_REPO_URL = "https://api.github.com/repos/hnanoto/CloverBootloader-Hackintosh-and-Beyond/releases/latest"

# URL de download direto (se você quiser forçar uma versão específica, descomente abaixo e comente o CLOVER_REPO_URL)
# CLOVER_DOWNLOAD_URL = "https://github.com/hnanoto/CloverBootloader-Hackintosh-and-Beyond/releases/download/5161/CloverV2-5161.zip"

# Tamanho mínimo aceitável para o arquivo Clover.zip (em bytes)
MIN_CLOVER_ZIP_SIZE = 1000000  # 1 MB

# Hash SHA256 esperado para o arquivo Clover.zip (para verificação de integridade)
# Você precisará calcular o hash do arquivo baixado e colocar aqui.
# Exemplo: CLOVER_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" # (hash SHA256 de um arquivo vazio)
CLOVER_SHA256 = ""  # Deixe em branco se não quiser verificar a integridade