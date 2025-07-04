import datetime
import json
import os
from config import LOGFILE, RED, GREEN, YELLOW, NC, SCRIPT_DIR
import locale

translations = {}  # Dicionário global para armazenar as traduções

def get_system_language():
    """Obtém o idioma preferido do sistema operacional."""
    try:
        # Obtém o idioma e a codificação do sistema
        system_locale = locale.getdefaultlocale()
        if system_locale[0]:
            # Retorna o código do idioma (por exemplo, 'pt_BR', 'en_US')
            return system_locale[0].split('_')[0]  # Retorna apenas o código principal (pt, en, etc.)
        else:
            # Retorna None se não conseguir obter o idioma
            return None
    except Exception as e:
        logger("error_getting_system_language", RED, error=e)
        return None

def load_translations(language=None):
    """Carrega as traduções de um arquivo JSON."""
    global translations
    if not language:
        language = get_system_language() or "en"  # Usa "en" como padrão se não conseguir detectar o idioma

    translations_path = os.path.join(SCRIPT_DIR, "translations")
    print(f"Tentando carregar traduções de: {translations_path}/{language}.json")
    try:
        with open(f"{translations_path}/{language}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            translations = data.get(language, {})
        if not translations and language != "en":
            logger("language_section_not_found", YELLOW, language=language)
            load_translations("en")
        else:
            logger(f"Traduções carregadas com sucesso para o idioma: {language}", GREEN)
    except FileNotFoundError:
        logger("translation_file_not_found", RED, language=language)
        # Carrega o idioma padrão (inglês) se o arquivo de tradução não for encontrado
        if language != "en":
            load_translations("en")
    except json.JSONDecodeError:
        logger("json_decode_error", RED, language=language)

def logger(message_key, color=None, return_message=False, **kwargs):
    """Registra mensagens de log no console e em um arquivo."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color_prefix = color if color else ""
    color_suffix = NC if color else ""

    # Obtém a mensagem traduzida ou usa a chave como mensagem padrão
    message = translations.get(message_key, message_key)

    # Formata a mensagem com argumentos nomeados, se houver
    try:
        message = message.format(**kwargs)
    except KeyError as e:
        logger("formatting_key_not_found", RED, key=e, message_key=message_key)
        return None

    log_message = f"[{timestamp}] {color_prefix}{message}{color_suffix}"

    if not return_message:
        print(log_message)
        with open(LOGFILE, "a", encoding="utf-8") as log_file:
            log_file.write(log_message + "\n")

    return message if return_message else log_message