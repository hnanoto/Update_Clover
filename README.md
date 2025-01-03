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
-   **[Seu Nome/Usuário GitHub]** -  pela criação desse script.

## Isenção de Responsabilidade

Este script é fornecido "como está", sem garantia de qualquer tipo. O autor e os contribuidores não se responsabilizam por quaisquer danos causados pelo uso deste script. Use por sua conta e risco. É sempre recomendável fazer um backup completo do seu sistema antes de fazer qualquer modificação.

---
Use code with caution.
Markdown
Instruções para o Repositório:

Crie um novo repositório no GitHub (ou use um existente).
Copie o código do script Python que desenvolvemos para um arquivo chamado Update_Clover.py dentro do seu repositório.
Copie o conteúdo do README acima para um arquivo chamado README.md na raiz do seu repositório.
Faça o commit e push das mudanças para o seu repositório.
