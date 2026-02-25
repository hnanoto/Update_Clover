#!/bin/bash

# Caminho até o diretório do script
cd "$(dirname "$0")"

# Verifica se o Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 não encontrado. Por favor, instale-o antes de continuar."
    exit 1
fi

# Instala as dependências automaticamente (se necessário)
echo "Verificando dependências..."
python3 -m pip install --quiet -r requirements.txt

# Executa o script principal
echo "Iniciando o Clover Updater..."
python3 main.py

