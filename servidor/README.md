# Rodar o app num servidor Windows da rede (Agendador de Tarefas)

O app roda como tarefa agendada: sobe junto com o Windows, sem ninguém logado, como a conta SYSTEM, e tenta reiniciar até 3 vezes se cair. Mesmo modelo do AppDOU (`instalar_servico.ps1` do pesquisa_diario). Nome do servidor, porta em uso e endereços internos: `_sessao/INTERNO.md`.

| Arquivo | Para quê |
|---|---|
| `instalar_tarefa.ps1` | Uma vez: cria o `.venv`, instala as dependências, registra a tarefa, abre a porta no firewall do Windows e sobe o app |
| `atualizar.ps1` | A cada versão nova: `git pull`, dependências, reinício |
| `iniciar.cmd` | O que a tarefa executa; a saída do app vai para `logs\app.log` |
| `comum.ps1` | Funções dos dois scripts |

## Primeira instalação

1. Python 3.10 ou mais novo no servidor (python.org, com "Add python.exe to PATH"). O script procura `py -3` e depois `python`.
2. No clone, copie `.env.example` para `.env` e preencha. Os nomes das variáveis mudam conforme a branch, e o `.env.example` não lista os opcionais (por exemplo, o que desliga o raciocínio do LLM local): a lista completa é a do código da branch, `grep -rn "getenv\|st.secrets\|_segredo(" --include=*.py .`, e a tabela de variáveis de `_sessao/INFRASTRUCTURE-REFERENCE.md`. Os valores internos estão em `_sessao/INTERNO.md`.
3. Num PowerShell **como Administrador**, na raiz do clone:

   ```powershell
   powershell -ExecutionPolicy Bypass -File servidor\instalar_tarefa.ps1 -Porta 8401
   ```

   O script termina mostrando o endereço (`http://<servidor>:8401/`) ou o erro. Pode rodar de novo sem duplicar nada.

## Atualizar

Depois de cada push no Gitea, no servidor, como Administrador:

```powershell
powershell -ExecutionPolicy Bypass -File servidor\atualizar.ps1 -Porta 8401
```

Ele recusa atualizar se houver alteração local em arquivo versionado (avisa em vez de descartar) e não reinicia nada se o `git pull` falhar.

## Dia a dia

- Ver se está no ar: `Get-ScheduledTask ChecklistConformidade` e `http://localhost:8401/_stcore/health` (responde `ok`).
- Parar ou subir: `Stop-ScheduledTask ChecklistConformidade` / `Start-ScheduledTask ChecklistConformidade`.
- Log: `logs\app.log` (cresce sem limite; pode apagar com o app parado).
- Mudou o `.env`? Rode o `atualizar.ps1`: o app só lê a configuração ao subir.
- Desinstalar: `Unregister-ScheduledTask ChecklistConformidade` e apagar a regra "checklist-conformidade (TCP 8401)" do firewall.
