# Update_Clover

# Update Clover Script

https://www.youtube.com/channel/UC-SkAYQyY0e49ALoOrdcOTQ

https://discord.gg/5hvZ5u7QXQ

Este script Python automatiza o processo de atualização do seu bootloader Clover para a versão mais recente disponível no repositório [hnanoto/CloverBootloader-Hackintosh-and-Beyond](https://github.com/hnanoto/CloverBootloader-Hackintosh-and-Beyond). Ele foi desenvolvido para simplificar e agilizar a atualização, tornando-a mais acessível para usuários da comunidade Hackintosh.

## Funcionalidades

-   **Verificação de Ambiente:** Verifica se o script está sendo executado no macOS.
-   **Verificação de Dependências:** Garante que as dependências necessárias (`curl`, `unzip`, `PlistBuddy`, `installer`) estejam instaladas.
-   **Download Automático:** Baixa a última versão do Clover do repositório [hnanoto/CloverBootloader-Hackintosh-and-Beyond](https://github.com/hnanoto/CloverBootloader-Hackintosh-and-Beyond).
-   **Detecção de Partições EFI:** Lista todas as partições EFI disponíveis e permite que você escolha qual deseja atualizar.
-   **Backup da EFI:** Cria um backup completo da sua partição EFI antes de realizar qualquer modificação. Os backups são armazenados na pasta `EFI_BACKUPS` dentro do diretório `HOME` do usuário, com nomes contendo a data e hora do backup. Os backups são nomeados sequencialmente se já existir um no mesmo minuto.
-   **Atualização dos Arquivos de Boot:** Atualiza os arquivos `BOOTX64.efi` e `CLOVERX64.efi` na sua partição EFI.
-   **Atualização de Drivers UEFI:** Atualiza os drivers UEFI existentes na pasta `EFI/CLOVER/Drivers/UEFI` da sua partição EFI, comparando-os com os drivers encontrados nas subpastas de `Drivers/Off/UEFI` (`FileSystem`, `FileVault2`, `HID`, `MemoryFix`, `Other`) do Clover baixado. **Importante:** O script sobrescreve apenas os drivers existentes; ele não adiciona novos drivers à sua EFI.
-   **Limpeza:** Remove os arquivos temporários baixados após a conclusão da atualização.
-   **Registro de Log:** Cria um arquivo de log detalhado (`update_clover_[timestamp].log`) no mesmo diretório do script, registrando todas as ações realizadas.

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

## Como Executar

1. **Baixe o Script:** Baixe o script `Update_Clover.py` do repositório.
2. **Torne o Script Executável:** Abra o Terminal e navegue até o diretório onde você baixou o script. Em seguida, execute o comando:
    
    ```bash
    chmod +x Update_Clover.py
    ```
    
3. **Execute o Script com Privilégios de Administrador:** Execute o script com `sudo` para garantir que ele tenha as permissões necessárias para modificar a partição EFI:
    
    ```bash
    sudo python3 Update_Clover.py
    ```
    
4. **Siga as Instruções na Tela:**
    
    -   O script listará as partições EFI detectadas. Digite o número correspondente à partição EFI que você deseja atualizar e pressione Enter.
    -   O script criará um backup da sua EFI e prosseguirá com a atualização.
    -   Acompanhe o progresso pelo log exibido no Terminal e pelo arquivo `update_clover_[timestamp].log` gerado na mesma pasta do script.

## Notas Importantes

-   **Backup:** Embora o script crie backups da sua EFI, é altamente recomendável que você também faça um backup manual da sua partição EFI antes de executar o script, como precaução extra.
-   **Permissões do Backup:** Os backups são criados com permissões que permitem que todos os usuários os leiam (diretórios: `0o755`, arquivos: `0o644`). Isso garante que usuários comuns possam acessar os backups, se necessário.
-   **Drivers UEFI:** O script **apenas atualiza os drivers UEFI existentes** na sua partição EFI. Ele **não adiciona novos drivers**. Certifique-se de que os drivers necessários para o seu sistema já estejam presentes na sua EFI antes de executar o script.
-   **Data de Modificação:** O script preserva a data de modificação original dos arquivos do Clover baixado. Portanto, os arquivos atualizados na sua EFI manterão as datas originais, que podem parecer "futuras" dependendo da data de lançamento da versão do Clover.
-   **Testado em:** O script foi testado em macOS(versão do macOS que vc testou).

## Solução de Problemas

-   **Erros de Permissão:** Se você encontrar erros relacionados a permissões, certifique-se de estar executando o script com `sudo`.
-   **Falha no Download:** Se o download do Clover falhar, verifique sua conexão com a internet e tente executar o script novamente.
-   **Partição EFI Não Montada:** Se o script informar que a partição EFI selecionada não está montada, monte-a manualmente usando o comando `diskutil mount <identificador_da_partição>` (por exemplo, `diskutil mount disk0s1`) e execute o script novamente.

## Contribuições

Contribuições para melhorar este script são bem-vindas! Sinta-se à vontade para abrir um *Pull Request* com suas modificações.

## Créditos

-   **Desenvolvedores do Clover:** Pelo excelente bootloader Clover.
-   **Comunidade Hackintosh:** Por todo o suporte e conhecimento compartilhado.
-   **[Henrique/hnanoto GitHub]** -  pela criação desse script.

## Isenção de Responsabilidade

Este script é fornecido "como está", sem garantia de qualquer tipo. O autor e os contribuidores não se responsabilizam por quaisquer danos causados pelo uso deste script. Use por sua conta e risco. É sempre recomendável fazer um backup completo do seu sistema antes de fazer qualquer modificação.



----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Update Clover Script

https://www.youtube.com/channel/UC-SkAYQyY0e49ALoOrdcOTQ

https://discord.gg/5hvZ5u7QXQ


This Python script automates the process of updating your Clover bootloader to the latest version available on the [hnanoto/CloverBootloader-Hackintosh-and-Beyond](https://github.com/hnanoto/CloverBootloader-Hackintosh-and-Beyond) repository. It's designed to simplify and streamline the update process, making it more accessible to users in the Hackintosh community.

## Features

-   **Environment Check:** Verifies that the script is being run on macOS.
-   **Dependency Check:** Ensures that the necessary dependencies (`curl`, `unzip`, `PlistBuddy`, `installer`) are installed.
-   **Automatic Download:** Downloads the latest Clover release from the [hnanoto/CloverBootloader-Hackintosh-and-Beyond](https://github.com/hnanoto/CloverBootloader-Hackintosh-and-Beyond) repository.
-   **EFI Partition Detection:** Lists all available EFI partitions and allows you to choose which one to update.
-   **EFI Backup:** Creates a full backup of your EFI partition before making any changes. Backups are stored in the `EFI_BACKUPS` folder within the user's `HOME` directory, with names containing the backup date and time. Backups are named sequentially if one already exists in the same minute.
-   **Boot File Update:** Updates the `BOOTX64.efi` and `CLOVERX64.efi` files on your EFI partition.
-   **UEFI Driver Update:** Updates existing UEFI drivers in the `EFI/CLOVER/Drivers/UEFI` folder of your EFI partition, comparing them with drivers found in the subfolders of `Drivers/Off/UEFI` (`FileSystem`, `FileVault2`, `HID`, `MemoryFix`, `Other`) from the downloaded Clover. **Important:** The script only overwrites existing drivers; it does not add new drivers to your EFI.
-   **Cleanup:** Removes temporary files downloaded after the update is complete.
-   **Logging:** Creates a detailed log file (`update_clover_[timestamp].log`) in the same directory as the script, recording all actions performed.

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

## How to Run

1. **Download the Script:** Download the `Update_Clover.py` script from the repository.
2. **Make the Script Executable:** Open Terminal and navigate to the directory where you downloaded the script. Then, run the command:

    ```bash
    chmod +x Update_Clover.py
    ```
3. **Run the Script with Administrator Privileges:** Execute the script with `sudo` to ensure it has the necessary permissions to modify the EFI partition:

    ```bash
    sudo python3 Update_Clover.py
    ```
4. **Follow the On-Screen Instructions:**

    -   The script will list the detected EFI partitions. Type the number corresponding to the EFI partition you want to update and press Enter.
    -   The script will create a backup of your EFI and proceed with the update.
    -   Monitor the progress through the log displayed in the Terminal and the `update_clover_[timestamp].log` file generated in the same folder as the script.

## Important Notes

-   **Backup:** Although the script creates backups of your EFI, it's highly recommended that you also manually back up your EFI partition before running the script, as an extra precaution.
-   **Backup Permissions:** Backups are created with permissions that allow all users to read them (directories: `0o755`, files: `0o644`). This ensures that regular users can access the backups if needed.
-   **UEFI Drivers:** The script **only updates existing UEFI drivers** on your EFI partition. It **does not add new drivers**. Make sure the drivers necessary for your system are already present in your EFI before running the script.
-   **Modification Date:** The script preserves the original modification date of the downloaded Clover files. Therefore, the updated files on your EFI will retain the original dates, which may appear to be in the "future" depending on the release date of the Clover version.
-   **Tested on:** The script has been tested on macOS (macOS version you tested).

## Troubleshooting

-   **Permission Errors:** If you encounter errors related to permissions, make sure you are running the script with `sudo`.
-   **Download Failure:** If the Clover download fails, check your internet connection and try running the script again.
-   **EFI Partition Not Mounted:** If the script reports that the selected EFI partition is not mounted, mount it manually using the command `diskutil mount <partition_identifier>` (for example, `diskutil mount disk0s1`) and run the script again.

## Contributions

Contributions to improve this script are welcome! Feel free to open a Pull Request with your modifications.

## Credits

-   **Clover Developers:** For the excellent Clover bootloader.
-   **Hackintosh Community:** For all the support and shared knowledge.
-   **[Henrique/GitHub hnanoto]** - for creating this script.


