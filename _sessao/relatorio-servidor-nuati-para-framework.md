---
para: sessão do nuati-framework (entregue pelo Rodrigo)
de: sessão do checklist-conformidade
data: 2026-10-01
assunto: levar um app Streamlit para o servidor do Nuati; pedido de recurso novo no framework
---

# Relatório e guia: app Streamlit no servidor do Nuati

> Marcadores: ✅ fato medido ou decidido (com fonte) · 📝 proposta do Claude, não validada.
> Nenhum dado interno aqui (servidor, IPs, caminhos de lá): ficam no `_sessao/INTERNO.md` de cada app.

## 1. O pedido

1. 📝 Absorver como **recurso do framework** a implantação de um app Streamlit no servidor do Nuati (Windows, Agendador de Tarefas), a partir da pasta `servidor/` do checklist, generalizada (seção 4). Nome sugerido: `servidor_nuati/`.
2. 📝 Pôr a receita da seção 5 no README do framework, §3, no lugar do passo 7 atual ("Servidor do Nuati: passa a espelhar `main`"), que hoje não diz como.
3. Depois, gerar o prompt para a sessão do buscador fazer o passe dela (insumos na seção 7). Pedido do Rodrigo, 01/10: *"vamos fazer isso com outros apps como o buscador... talvez seja o caso de ser mais uma feature no framework"*.

## 2. Evidência

- ✅ **D-C22** (Rodrigo, 29/09): o servidor do Nuati espelha a `main`.
- ✅ **Pedido do Rodrigo (01/10):** rodar o app no servidor em vez do Streamlit Cloud, por tarefa agendada, puxando do Gitea.
- ✅ **Base:** `pesquisa_diario/instalar_servico.ps1` (AppDOU). O README do framework, §6, já o citava como "fora por enquanto, útil para o servidor do Nuati, não lido a fundo".
- ✅ **Código** (checklist, Gitea): `servidor/` em `13bc7dc` + `9be45e2` na `homologacao`; na `main`, `8de4e7b` + `764f567` (cherry-pick só da pasta, opção `1a` do Rodrigo).
- ✅ **Teste nesta máquina** (worktree da `main`, sem administrador): `.venv` criado, dependências instaladas, `iniciar.cmd` subiu, `/_stcore/health` = `ok`, parada pela porta liberou.
- ✅ **No servidor** (Rodrigo, 01/10):
  - 1ª tentativa: o script **recusou** a porta 8400, ocupada por outro app Streamlit que não constava na lista de portas liberadas. Não derrubou o outro app.
  - 2ª tentativa, porta 8401: tarefa registrada, regra de firewall criada, app no ar.
  - De outra máquina da rede: health `ok`, página 200.
  - Uma geração com o Gemini funcionou.
- ✅ **O LLM local estourou o tempo (300 s).** Não é defeito da implantação: a `main` do checklist manda o normativo inteiro numa chamada só (o LM Studio respondeu a uma chamada mínima em 0,75 s). Fica no TODO do checklist.

## 3. Como funciona hoje (checklist, `servidor/`)

| Arquivo | Faz |
|---|---|
| `instalar_tarefa.ps1` | Uma vez, como Administrador. Acha o Python 3.10+ (`py -3`, depois `python`; recusa o atalho da Microsoft Store), cria o `.venv`, instala o `requirements.txt` e exige o `.env`. Depois registra a tarefa `ChecklistConformidade` (SYSTEM, ao iniciar o Windows, até 3 reinícios, sem limite de tempo, `IgnoreNew`), cria a regra de firewall do Windows, sobe o app e espera o health. Pode rodar de novo sem duplicar nada. |
| `atualizar.ps1` | A cada promoção, como Administrador. Recusa se houver alteração local em arquivo versionado. Faz `git pull --ff-only` (se falhar, não reinicia nada), reinstala as dependências, reinicia a tarefa, espera o health e mostra os commits que entraram. |
| `iniciar.cmd` | O que a tarefa executa: `cd` na raiz, `PYTHONIOENCODING=utf-8`, `streamlit run app.py --server.port <p> --server.address 0.0.0.0 --server.headless true`. A saída vai para `logs\app.log`. |
| `comum.ps1` | `Exigir-Admin`; `Parar-App`, que só mata, na porta, processos com `streamlit` e `--server.port <p>` na linha de comando e recusa qualquer outro programa; `Esperar-App` (health); `Instalar-Dependencias`. |
| `README.md` | Instalar, atualizar, dia a dia, desinstalar. |

Escolhas: `.ps1` só em ASCII e com CRLF (`.gitattributes`); `logs/` no `.gitignore`.

## 4. O que muda para virar recurso (📝)

1. **Tirar o que é do checklist do código.**
   - Hoje estão fixos: o nome da tarefa, a porta padrão, o `app.py` na raiz e o `requirements.txt` na raiz.
   - 📝 Proposta: um arquivo por app, nunca copiado do framework, como o `publicar_snapshot.conf`. Por exemplo `servidor_nuati.conf` (formato `chave=valor`, lido pelo PowerShell) com `NOME_TAREFA`, `PORTA`, `PASTA_APP` (relativa à raiz do repo), `ARQUIVO_APP` e `REQUIREMENTS`.
   - O buscador precisa disso: o app dele fica em `levantamento-normativos/app.py`, com o `requirements.txt` dentro dessa pasta.
2. **Configuração do app: aceitar `.env` ou `.streamlit/secrets.toml`.**
   - O checklist chama `load_dotenv()`, então lê o `.env`.
   - ✅ O buscador não chama `load_dotenv` em lugar nenhum (`git grep` na `main` de lá, 01/10). No servidor, ele dependeria do `secrets.toml`.
   - 📝 A conferir na documentação do Streamlit: ele lê o `.streamlit/secrets.toml` da pasta de onde o app é rodado e o `~/.streamlit/` do usuário. Como a tarefa roda como SYSTEM, o `~` é o perfil do sistema, não o do Rodrigo. Por isso o segredo tem de ficar na pasta do app.
   - Pela mesma razão, o `iniciar.cmd` deve fazer `cd` para a `PASTA_APP`, não para a raiz.
3. **De onde o servidor puxa.**
   - O checklist tem origem no Gitea.
   - ✅ O buscador tem origem no GitHub, com a Câmara como espelho (decidido em 22/09, `SESSION-ONBOARD-buscador.md`). A URL do espelho dele não está registrada (B-06 de lá).
   - Antes do passe, decidir se o servidor clona do espelho no Gitea, que então precisa receber push a cada promoção, ou do GitHub (repo privado, exige credencial no servidor). 📝 Recomendo o Gitea, que é o que a D-C22 descreve.
4. **Portas.**
   - ✅ A lista de portas liberadas do servidor não diz quais estão em uso: a 8400 estava ocupada por um app fora dela.
   - 📝 Manter um registro único de porta por app, no lugar onde o framework guarda dados internos (`segredos.exemplo.toml` ou equivalente, F-P3), e conferir no servidor antes de escolher (comando na seção 5).
5. **Log sem limite.** O `logs\app.log` só cresce. 📝 Rodar o log ao subir (por exemplo, renomear para `.1` acima de N MB) ou documentar a limpeza.
6. **Testes, no padrão F-P1** (`test_*.py` sem rede).
   - 📝 Proposta: um teste que roda o parser do PowerShell nos `.ps1`; um que confere que os `.ps1` são ASCII; e um que sobe um processo qualquer escutando numa porta e confere que o `Parar-App` se **recusa** a matá-lo.
   - Registrar tarefa e firewall exige administrador: fica como conferência manual no passe.
7. **Atualização automática: não por enquanto.**
   - ✅ Decidido no checklist em 01/10: atualizar é manual, com o `atualizar.ps1`.
   - 📝 Um pull automático exigiria credencial do Gitea para a conta SYSTEM e poria no ar todo push na `main` sem revisão.

## 5. Guia da promoção para o servidor (proposta de texto para o README §3)

Quem faz: **(C)** a sessão do Claude no app · **(R)** o Rodrigo, no servidor, num PowerShell **como Administrador**.

### Primeira vez (por app)

1. **(R) Escolher uma porta livre** dentro da faixa liberada:
   ```powershell
   8400..8408 | % { $c = Get-NetTCPConnection -State Listen -LocalPort $_ -ErrorAction SilentlyContinue; "$_ : " + $(if ($c) { "ocupada" } else { "livre" }) }
   ```
2. **(C) Adotar o recurso.**
   - Copiar a pasta do framework e criar o `.conf` do app (porta, pasta, nome da tarefa).
   - Commit na `homologacao`; levar à `main` só a pasta e o `.conf`, com o ok do Rodrigo.
   - Push no Gitea (e no espelho, se a origem for o GitHub).
   - Registrar servidor, pasta e porta no `_sessao/INTERNO.md` do app.
3. **(R) Clonar do Gitea, branch `main`, numa pasta curta** (por exemplo `E:\apps\<app>`). ✅ Caminho longo quebra o `pip` com WinError 206.
4. **(R) Criar a configuração.**
   - Usar os nomes que o código da **`main`** lê. ✅ O `.env.example` não basta: no checklist ele não lista o opcional que desliga o raciocínio do LLM local (`LOCAL_LLM_DISABLE_THINKING` na `main` antiga; `LLM_DISABLE_THINKING` no `llm_cadeia`, tabela "Segredos" do `llm_cadeia/README.md`), e o Rodrigo preencheu só o que estava no exemplo. Lista completa: `grep -rn "getenv\|st.secrets\|_segredo(" --include=*.py .` na `main`. 📝 O recurso poderia trazer um exemplo do bloco do servidor. Os valores internos estão no `INTERNO.md`.
   - Antes, conferir que o servidor alcança o LLM: `Invoke-RestMethod <LLM_BASE_URL>/models`.
5. **(R) Instalar:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File <pasta-do-recurso>\instalar_tarefa.ps1
   ```
   O script termina com o endereço ou com o erro.
6. **(R+C) Conferir.**
   - De outra máquina da rede: `http://<servidor>:<porta>/_stcore/health` responde `ok`.
   - Uma geração curta com cada provedor configurado.
   - Registrar no `log.md` do app quem respondeu, o tempo e o resultado.

### A cada promoção

1. **(C, com o ok do Rodrigo):**
   - `homologacao` → `main`, com tag;
   - push da `main` no Gitea (e no espelho);
   - snapshot da `main` no GitHub (Streamlit de produção), sempre com `--simular` antes.
2. **(R) No servidor:** se a versão nova lê nomes de configuração diferentes (no checklist, a ida do framework à `main` troca `LOCAL_LLM_*`/`GEMINI_MODEL` pelos nomes do `llm_cadeia`), reescrever o `.env` ou o `secrets.toml` **antes**; depois, rodar `atualizar.ps1`. ✅ O servidor **não** atualiza sozinho.
3. **(R+C)** Health e uma geração curta.

### Voltar atrás

Pela regra do §3: commit de reversão na `main` (`git revert`), nunca push forçado; depois, `atualizar.ps1` no servidor. O `--ff-only` do script recusa uma `main` reescrita, e é isso que se quer.

### Mudou só a configuração

O app só lê o `.env` ou o `secrets.toml` ao subir: rode o `atualizar.ps1` (ele reinicia mesmo sem código novo).

## 6. Pegadinhas medidas no checklist (✅, `LICOES.md` de lá, 01/10)

- **Levar só a pasta para a `main` por cherry-pick tira a `main` da linha da `homologacao`:** na promoção seguinte, o `git merge --ff-only` do README §3 falha; o merge normal sai limpo. A receita do §3 deveria prever isso.
- **Caminho longo:** o `pip install` falha com WinError 206 (o numpy tem pastas fundas). Use pasta curta.
- **O `python.exe` de um `.venv` no Windows é um lançador:** quem escuta na porta pode ser o Python base, como processo filho. Identifique o Streamlit pela linha de comando, não pelo caminho do executável.
- **O PowerShell 5.1 lê `.ps1` sem BOM como ANSI:** acento quebra. Use só ASCII nos scripts.
- **A lista de portas liberadas não diz quais estão em uso:** confira antes (passo 1).
- **Push para o Gitea a partir de um subagente falha** com "Authentication failed". Na sessão principal, funciona (credencial em cache).
- **Mudança no `.env` só vale depois de reiniciar** (`atualizar.ps1`).

## 7. Insumos para o prompt da sessão do buscador

- **App:** `levantamento-normativos/app.py`, com o `requirements.txt` na mesma pasta (precisa do `PASTA_APP` da seção 4.1).
- **Configuração:** sem `load_dotenv`, então `.streamlit/secrets.toml` dentro de `levantamento-normativos/` (seção 4.2, a conferir). Para o servidor, o bloco inclui `LLM_BASE_URL`/`LLM_MODEL` (D-C19: mesmo código no servidor e no Cloud, só os segredos mudam).
- **Origem:** GitHub, com espelho no Gitea. A URL do espelho falta (B-06): resolver antes do passe (seção 4.3).
- **Porta:** livres em 01/10: 8404 a 8408 (8401 = checklist, 8400 e 8403 ocupadas, 8402 = Gerador de Matriz). Conferir de novo no dia.
- **LLM local:** 📝 o buscador faz requisições pequenas (lotes de 20, `LICOES.md` do checklist, 25/09), então o estouro de 300 s visto no checklist não deve se repetir. Conferir no passo 6.
