#!/usr/bin/env bash
# Publica no GitHub (repo PUBLICO; o Streamlit Cloud publica o app a partir dele) um snapshot
# do master local SEM os arquivos internos. O historico completo fica so no GitLab interno.
# Uso (raiz do repo): bash scripts/publicar_github.sh [--simular]
set -euo pipefail

EXCLUIR=(
  "_sessao/INTERNO.md"
)

git fetch github
indice=$(mktemp)
trap 'rm -f "$indice"' EXIT
GIT_INDEX_FILE="$indice" git read-tree master
for caminho in "${EXCLUIR[@]}"; do
  GIT_INDEX_FILE="$indice" git rm -r --cached --quiet --ignore-unmatch -- "$caminho"
done
arvore=$(GIT_INDEX_FILE="$indice" git write-tree)

# Trava de seguranca: nenhum dado de infraestrutura interna pode ir junto.
if git grep -n -E '10[.]10[.]111|10[.]1[.]3[.]11|nuati[.]secin|Alexa[n]dro|git[.]camara[.]gov[.]br' "$arvore" -- .; then
  echo "ABORTADO: dado interno encontrado no snapshot (acima). Mova-o para _sessao/INTERNO.md." >&2
  exit 1
fi

if [ "$arvore" = "$(git rev-parse 'github/master^{tree}')" ]; then
  echo "GitHub ja esta atualizado."
  exit 0
fi

if [ "${1:-}" = "--simular" ]; then
  echo "SIMULACAO: arquivos que mudariam no GitHub (nada foi enviado):"
  git diff --stat github/master "$arvore" | tail -25
  exit 0
fi

mensagem="Snapshot publico de $(git rev-parse --short master) ($(date +%F))"
commit=$(git commit-tree "$arvore" -p github/master -m "$mensagem")
git push github "$commit:refs/heads/master"
echo "Publicado: $commit (Streamlit Cloud vai republicar o app)"
