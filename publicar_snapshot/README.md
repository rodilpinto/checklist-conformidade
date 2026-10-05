# publicar_snapshot: repo interno → snapshot público no GitHub (pasta copiável)

**Versão 1.0.1** (`VERSAO` no script; `--versao` imprime) · **Origem:** `github.com/rodilpinto/nuati-framework`
(privado), pasta `publicar_snapshot/`. Histórico: [`CHANGELOG.md`](CHANGELOG.md).

Para app cuja **origem é o servidor git interno** (histórico completo, notas internas) e que precisa de uma cópia
**pública** no GitHub para o Streamlit Cloud. O script monta um snapshot da branch sem os arquivos internos, roda uma
trava que procura dado interno (IP, login, host) no que vai sair e só então empurra um commit novo para o GitHub. O
histórico interno nunca sai.

Não serve para app cuja origem já é o GitHub (buscador, scopediagram): esses empurram direto.

## Adotar num app

1. **Copie a pasta inteira** `publicar_snapshot/` para a raiz do app, sem editar nada, e registre a cópia no README da
   raiz do framework ("Registro de cópias").
2. Copie `publicar_snapshot.conf.example` para **`publicar_snapshot.conf` na raiz do app** e preencha:
   `EXCLUIR` (o que fica só no servidor interno) e `TRAVA` (padrões de dado interno; valores reais no
   `segredos.exemplo.toml` da raiz do framework). O `.conf` nunca vai para o snapshot.
3. O remoto do GitHub precisa existir (padrão `github`): `git remote add github https://github.com/<dono>/<app>.git`.
4. Use, da raiz do app:

```bash
bash publicar_snapshot/publicar_snapshot.sh --simular                 # o que mudaria; nada é enviado
bash publicar_snapshot/publicar_snapshot.sh                           # publica a RAMO_PADRAO (main)
bash publicar_snapshot/publicar_snapshot.sh --ramo homologacao        # publica a homologacao
```

5. Rode, da pasta que contém `publicar_snapshot/`: `python -m pytest publicar_snapshot -q` (precisa de bash e git; no
   Windows, o bash do Git).

## Como funciona

| Passo | Detalhe |
|---|---|
| Snapshot | índice temporário com a árvore da branch, menos `EXCLUIR` e o `.conf` |
| Trava | `git grep -E` de todos os `TRAVA` na árvore (menos `TRAVA_EXCETO`); achou → aborta com status 1 e mostra onde; erro do grep também aborta |
| Base | a própria branch no GitHub; se não existe, a `RAMO_PADRAO` de lá; se nada existe, primeiro snapshot (sem pai) |
| Envio | um commit "Snapshot publico de <branch> @ <hash> (<data>)" em cima da base; push sem força |

Saídas: 0 publicado ou já atualizado; 1 trava; 2 erro de uso (falta `.conf`, branch inexistente, argumento).

## Com D-C22 (main + homologacao)

App com dois remotos: o Streamlit lê **só o GitHub**. Depois de cada push no servidor interno, rode o script para a
branch que mudou. `main` alimenta o app de produção; `homologacao`, o de homologação. Receita completa de ambientes:
README da raiz do framework.

## Regra de sincronia

**Não edite uma cópia.** O que é do app fica no `publicar_snapshot.conf` dele. Melhoria nasce no framework, sobe
`VERSAO`, entra no `CHANGELOG.md` e é recopiada.
