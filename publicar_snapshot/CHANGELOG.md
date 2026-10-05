# Changelog do publicar_snapshot

Versão atual: `VERSAO` em `publicar_snapshot.sh`.

## 1.0.1 (01/10/2026): publicar outra branch com arquivo excluído diferente

Pedido 6.1 do passe por app do checklist (relatório de 01/10): com `homologacao` aberta,
`--ramo master` abortava com "the following file has staged content different from both the file and the HEAD:
_sessao/INTERNO.md". Causa: o `git rm --cached` no índice temporário comparava com a branch aberta e a pasta de
trabalho. Conserto: `-f` nesse `git rm` (só mexe no índice temporário; a branch aberta e a pasta de trabalho não são
tocadas). Teste novo reproduz o caso (falhava antes, passa agora). Quem usou o contorno do `git worktree` pode voltar
a rodar o script direto.

## 1.0.0 (30/09/2026): entra no nuati-framework, generalizado

Nasceu de `checklist-conformidade/scripts/publicar_github.sh`, branch `feat/llm-cadeia` @ `92ac158` (servidor
interno). A lógica é a mesma (índice temporário → `write-tree` → trava com `git grep` → `commit-tree` → push). 📝 Mudanças
propostas pelo Claude para a peça poder ser copiada sem edição:

- Tudo que era do checklist saiu do script para o `publicar_snapshot.conf` do app: `EXCLUIR`, os padrões da trava
  (`TRAVA`), as exceções (`TRAVA_EXCETO`), o remoto e a branch padrão. O `.conf` é sempre excluído do snapshot.
- Branch padrão `main` (D-C22), em vez de `master`.
- Primeiro snapshot funciona sem branch alguma no GitHub (o original exigia `github/master`).
- Erro do `git grep` (status > 1) aborta. No original, um erro caía no mesmo caminho de "nada encontrado" e o push
  seguia.
- A exceção da trava para `llm_cadeia/` (decisão de 28/09) não é mais necessária: a 1.1.0 do `llm_cadeia` não tem dado
  interno. Se um app ainda tiver a cópia 1.0.x, ponha `llm_cadeia/` em `TRAVA_EXCETO` até o passe por app.
- `--versao`; mensagens de erro de uso com status 2.

Testes novos (8): rodam o script de verdade em repos descartáveis, com um repo local no papel do GitHub.
