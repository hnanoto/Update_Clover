# Update Clover Script

Este script Python automatiza o processo de atualização do seu bootloader Clover para a versão mais recente disponível no repositório [hnanoto/CloverBootloader-Hackintosh-and-Beyond](https://github.com/hnanoto/CloverBootloader-Hackintosh-and-Beyond). Ele foi desenvolvido para simplificar e agilizar a atualização, tornando-a mais acessível para usuários da comunidade Hackintosh.

## Funcionalidades

-   **Detecção Automática de Idioma:** O script agora detecta automaticamente o idioma do sistema (Português ou Inglês) e exibe as mensagens no idioma correspondente. As mensagens são armazenadas em arquivos JSON separados na pasta `translations` para facilitar a tradução para outros idiomas.
-   **Menu Interativo:** Um menu interativo permite que você escolha quais componentes atualizar:
    -   **Atualizar BOOTX64.efi e CLOVERX64.efi:** Atualiza apenas os arquivos de inicialização principais do Clover.
    -   **Atualizar Drivers:** Atualiza apenas os drivers UEFI na pasta `EFI/CLOVER/Drivers/UEFI`.
    -   **Atualização Completa:** Atualiza os arquivos de inicialização e os drivers UEFI.
    -   **Sair:** Sai do script.
-   **Verificação de Ambiente:** Verifica se o script está sendo executado no macOS.
-   **Verificação de Dependências:** Garante que as dependências necessárias (`curl`, `unzip`, `/usr/libexec/PlistBuddy`, `installer`) estejam instaladas.
-   **Download Inteligente:** Baixa a última versão do Clover apenas uma vez e a reutiliza para todas as operações de atualização, economizando tempo e largura de banda.
-   **Detecção de Bootloader:** Verifica se a partição EFI selecionada contém uma instalação do Clover. Se o OpenCore ou o Gerenciador de Boot do Windows forem detectados, o script aborta a operação para evitar danos.
-   **Espera por Montagem:** Se a partição EFI selecionada não estiver montada, o script aguarda até que você a monte manualmente. Ele fornece instruções claras e permite que você continue a atualização assim que a partição estiver pronta.
-   **Backup da EFI:** Cria um backup completo da sua partição EFI antes de realizar qualquer modificação. Os backups são armazenados na pasta `EFI_BACKUPS` dentro do diretório `HOME` do usuário, com nomes contendo a data e hora do backup. Os backups são nomeados sequencialmente se já existir um no mesmo minuto.
-   **Atualização Segura:** O script verifica se a partição EFI está montada como leitura/gravação antes de tentar atualizá-la.
-   **Tratamento de Erros:** O script captura erros e exibe mensagens de erro claras e informativas. Um tipo de exceção personalizado `CloverUpdateError` é usado para erros específicos do script.
-   **Log Detalhado:** Cria um arquivo de log detalhado (`update_clover_[timestamp].log`) no mesmo diretório do script, registrando todas as ações realizadas, incluindo mensagens de sucesso, avisos e erros.
-   **Limpeza:** Remove os arquivos temporários baixados após a conclusão da atualização.
-   **Internacionalização:** Suporte para mensagens em Português (pt-BR) e Inglês (en-US). O idioma é detectado automaticamente com base nas configurações do sistema, mas o Português será usado como padrão se a detecção falhar ou se o idioma do sistema não tiver um arquivo de tradução correspondente.

## Pré-requisitos

-   **macOS:** O script foi desenvolvido para ser executado no macOS.
-   **Python 3:** Certifique-se de ter o Python 3 instalado. Você pode verificar digitando `python3 --version` no terminal.
-   **Dependências:** O script depende dos seguintes comandos:
    -   `curl`
    -   `unzip`
    -   `/usr/libexec/PlistBuddy`
    -   `installer`

    Esses comandos geralmente estão pré-instalados no macOS. O script irá verificar se eles estão disponíveis antes de prosseguir.
-   **Conexão com a Internet:** Uma conexão ativa com a internet é necessária para baixar a última versão do Clover.
-   **Partição EFI Montada:** **A partição EFI que você deseja atualizar deve estar montada e acessível para escrita antes de executar o script.** Você pode montar a partição EFI manualmente usando o comando `diskutil mount <identificador_da_partição>` (por exemplo, `diskutil mount disk0s1`) no Terminal.

## Como Executar

1. **Baixe o Script:** Baixe o script `main.py` e os arquivos e pastas `clover_updater.py`, `config.py`, `efi_handler.py`, `logger.py`, `menu.py`, `utils.py`, e a pasta `translations` do repositório.
2. **Descompacte o arquivo zip e coloque os arquivos na mesma pasta em um diretório de sua escolha, exemplo: `update_clover`.**
3. **Torne o Script Executável:** Abra o Terminal e navegue até o diretório onde você baixou o script, exemplo: `cd update_clover`. Em seguida, execute o comando:

    ```bash
    chmod +x main.py
    ```

4. **Execute o Script com Privilégios de Administrador:** Execute o script com `sudo` para garantir que ele tenha as permissões necessárias para modificar a partição EFI:

    ```bash
    sudo python3 main.py
    ```

5. **Siga as Instruções na Tela:**

    -   O script listará as partições EFI detectadas. Digite o número correspondente à partição EFI que você deseja atualizar e pressione Enter.
    -   **Certifique-se de que a partição EFI correta esteja montada antes de prosseguir.**
    -   Se a partição EFI não estiver montada, o script aguardará até que você a monte manualmente.
    -   O script criará um backup da sua EFI e, em seguida, exibirá um menu com as opções de atualização.
    -   Escolha a opção desejada e pressione Enter.
    -   Acompanhe o progresso pelo log exibido no Terminal e pelo arquivo `update_clover_[timestamp].log` gerado na mesma pasta do script.

## Menu Interativo

O menu interativo oferece as seguintes opções:

1. **Atualizar BOOTX64.efi e CLOVERX64.efi:** Atualiza os arquivos de boot principais do Clover.
2. **Atualizar Drivers:** Atualiza os drivers UEFI na pasta `EFI/CLOVER/Drivers/UEFI`.
3. **Atualização Completa:** Atualiza os arquivos de boot e os drivers UEFI.
4. **Sair:** Sai do script.

## Notas Importantes

-   **Backup:** Embora o script crie backups da sua EFI, é altamente recomendável que você também faça um backup manual da sua partição EFI antes de executar o script, como precaução extra.
-   **Drivers UEFI:** O script **apenas atualiza os drivers UEFI existentes** na sua partição EFI. Ele **não adiciona novos drivers**. Certifique-se de que os drivers necessários para o seu sistema já estejam presentes na sua EFI antes de executar o script.
-   **Data de Modificação:** O script preserva a data de modificação original dos arquivos do Clover baixado. Portanto, os arquivos atualizados na sua EFI manterão as datas originais, que podem parecer "futuras" dependendo da data de lançamento da versão do Clover.
-   **Testado em:** O script foi testado em macOS (versão do macOS que vc testou).

## Solução de Problemas

-   **Erros de Permissão:** Se você encontrar erros relacionados a permissões, certifique-se de estar executando o script com `sudo`.
-   **Falha no Download:** Se o download do Clover falhar, verifique sua conexão com a internet e tente executar o script novamente.
-   **Partição EFI Não Montada:** Se o script informar que a partição EFI selecionada não está montada, **monte-a manualmente usando o comando `diskutil mount <identificador_da_partição>` e execute o script novamente.** O script aguardará até que a partição seja montada antes de continuar.
-   **Partição EFI Somente Leitura:** Se você receber mensagens de erro indicando que a partição EFI está montada como somente leitura, tente desmontá-la e montá-la novamente. Se o problema persistir, pode ser necessário investigar problemas específicos do seu sistema ou buscar ajuda especializada na comunidade Hackintosh.

## Contribuições

Contribuições para melhorar este script são bem-vindas! Sinta-se à vontade para abrir um *Pull Request* com suas modificações.

## Créditos

-   **Desenvolvedores do Clover:** Pelo excelente bootloader Clover.
-   **Comunidade Hackintosh:** Por todo o suporte e conhecimento compartilhado.
-   **[Henrique/hnnanoto GitHub]** - pela criação desse script.

## Isenção de Responsabilidade

Este script é fornecido "como está", sem garantia de qualquer tipo. O autor e os contribuidores não se responsabilizam por quaisquer danos causados pelo uso deste script. Use por sua conta e risco. É sempre recomendável fazer um backup completo do seu sistema antes de fazer qualquer modificação.

---

## Atualização para Detecção Automática de Idioma

O script foi atualizado para suportar tradução de mensagens de texto para diferentes idiomas. Atualmente, ele suporta Português e Inglês.

### Como o Script Detecta o Idioma

O script utiliza a função `locale.getdefaultlocale()` para obter o idioma preferido do sistema operacional do usuário. Com base nisso, ele tenta carregar as mensagens traduzidas do arquivo JSON correspondente na pasta `translations`.

-   Se o script encontrar um arquivo de tradução para o idioma do sistema (por exemplo, `pt.json` para Português), ele carregará as mensagens desse arquivo.
-   Se nenhum arquivo de tradução for encontrado para o idioma do sistema, o script usará as mensagens padrão em inglês.



----------------------------------------------------------------------------------------------------------------------------------------------------------------
Update Clover Script

This Python script automates the process of updating your Clover bootloader to the latest version available on the [hnanoto/CloverBootloader-Hackintosh-and-Beyond](https://github.com/hnanoto/CloverBootloader-Hackintosh-and-Beyond) repository. It's designed to simplify and streamline the update process, making it more accessible to users in the Hackintosh community.

## Features

-   **Automatic Language Detection:** The script now automatically detects the system language (Portuguese or English) and displays messages in the corresponding language.
-   **Interactive Menu:** An interactive menu allows you to choose which components to update:
    -   **Update BOOTX64.efi and CLOVERX64.efi:** Updates only the main Clover boot files.
    -   **Update Drivers:** Updates only the UEFI drivers in the `EFI/CLOVER/Drivers/UEFI` folder.
    -   **Full Update:** Updates all components (boot files and UEFI drivers).
-   **Environment Check:** Verifies that the script is being run on macOS.
-   **Dependency Check:** Ensures that the necessary dependencies (`curl`, `unzip`, `/usr/libexec/PlistBuddy`, `installer`) are installed.
-   **Smart Download:** Downloads the latest version of Clover only once, even if you perform multiple update operations, saving time and bandwidth.
-   **Bootloader Detection:** Verifies if the selected EFI partition contains a Clover installation. If OpenCore or the Windows Boot Manager is detected, the script aborts the operation to prevent damage.
-   **Wait for Mount:** If the selected EFI partition is not mounted, the script waits until you mount it manually. It provides clear instructions and allows you to continue the update as soon as the partition is ready.
-   **EFI Backup:** Creates a full backup of your EFI partition before making any modification. Backups are stored in the `EFI_BACKUPS` folder within the user's `HOME` directory, with names containing the backup date and time. Backups are named sequentially if one already exists in the same minute.
-   **Safe Update:** The script verifies that the EFI partition is mounted as read/write before attempting to update it.
-   **Error Handling:** The script captures errors and displays clear and informative error messages. A custom exception type `CloverUpdateError` is used for script-specific errors.
-   **Detailed Logging:** Creates a detailed log file (`update_clover_[timestamp].log`) in the same directory as the script, recording all actions performed.
-   **Cleanup:** Removes temporary files downloaded after the update is complete.
-   **Internationalization:** Support for messages in Portuguese (pt-BR) and English (en-US). The language is automatically detected based on system settings, but Portuguese will be used as default if detection fails or if there is no corresponding translation file for the system language.

## Prerequisites

-   **macOS:** The script is designed to run on macOS.
-   **Python 3:** Make sure you have Python 3 installed. You can verify this by typing `python3 --version` in the terminal.
-   **Dependencies:** The script relies on the following commands:
    -   `curl`
    -   `unzip`
    -   `/usr/libexec/PlistBuddy`
    -   `installer`

    These commands are usually pre-installed on macOS. The script will check if they are available before proceeding.
-   **Internet Connection:** An active internet connection is required to download the latest Clover release.
-   **Mounted EFI Partition:** **The EFI partition you want to update must be mounted and accessible for writing before running the script.** You can mount the EFI partition manually using the command `diskutil mount <partition_identifier>` (for example, `diskutil mount disk0s1`) in the Terminal.

## How to Run

1. **Download the Script:** Download the script `main.py` and the files and folders: `clover_updater.py`, `config.py`, `efi_handler.py`, `logger.py`, `menu.py`, `utils.py`, and the `translations` folder from the repository.
2. **Unzip the file and place the files in the same folder in a directory of your choice, for example: `update_clover`.**
3. **Make the Script Executable:** Open Terminal and navigate to the directory where you downloaded the script, for example: `cd update_clover`. Then, run the command:

    ```bash
    chmod +x main.py
    ```

4. **Run the Script with Administrator Privileges:** Execute the script with `sudo` to ensure it has the necessary permissions to modify the EFI partition:

    ```bash
    sudo python3 main.py
    ```

5. **Follow the On-Screen Instructions:**

    -   The script will list the detected EFI partitions. Type the number corresponding to the EFI partition you want to update and press Enter.
    -   **Make sure the correct EFI partition is mounted before proceeding.**
    -   If the EFI partition is not mounted, the script will wait until you mount it.
    -   The script will create a backup of your EFI and then display a menu with update options.
    -   Choose the desired option and press Enter.
    -   Monitor the progress through the log displayed in the Terminal and the `update_clover_[timestamp].log` file generated in the same folder as the script.

## Interactive Menu

The interactive menu offers the following options:

1. **Update BOOTX64.efi and CLOVERX64.efi:** Updates the main Clover boot files.
2. **Update Drivers:** Updates the UEFI drivers in the `EFI/CLOVER/Drivers/UEFI` folder.
3. **Full Update:** Updates both boot files and UEFI drivers.
4. **Exit:** Quits the script.

## Important Notes

-   **Backup:** Although the script creates backups of your EFI, it's highly recommended that you also manually back up your EFI partition before running the script, as an extra precaution.
-   **UEFI Drivers:** The script **only updates existing UEFI drivers** on your EFI partition. It **does not add new drivers**. Make sure the drivers necessary for your system are already present in your EFI before running the script.
-   **Modification Date:** The script preserves the original modification date of the downloaded Clover files. Therefore, the updated files on your EFI will retain the original dates, which may appear to be in the "future" depending on the release date of the Clover version.
-   **Tested on:** The script has been tested on macOS Ventura 13.6.3.

## Troubleshooting

-   **Permission Errors:** If you encounter errors related to permissions, make sure you are running the script with `sudo`.
-   **Download Failure:** If the Clover download fails, check your internet connection and try running the script again.
-   **EFI Partition Not Mounted:** If the script reports that the selected EFI partition is not mounted, **mount it manually using the command `diskutil mount <partition_identifier>` and run the script again.** The script will wait until the partition is mounted before continuing.
-   **EFI Partition Read-Only:** If you receive error messages indicating that the EFI partition is mounted as read-only, try unmounting and mounting it again. If the problem persists, you may need to investigate specific issues with your system or seek expert help from the Hackintosh community.

## Contributions

Contributions to improve this script are welcome! Feel free to open a Pull Request with your modifications.

## Credits

-   **Clover Developers:** For the excellent Clover bootloader.
-   **Hackintosh Community:** For all the support and shared knowledge.
-   **Henrique/hnanoto:** For creating this script.

## Disclaimer

This script is provided "as is", without warranty of any kind. The author and contributors are not responsible for any damage caused by the use of this script. Use at your own risk. It's always recommended to make a full backup of your system before making any modifications.

---

## Update for Automatic Language Detection

The script has been updated to support translation of text messages into different languages. It currently supports Portuguese and English.


-   **Clover Developers:** For the excellent Clover bootloader.
-   **Hackintosh Community:** For all the support and shared knowledge.
-   **[Henrique/GitHub hnanoto]** - for creating this script.


