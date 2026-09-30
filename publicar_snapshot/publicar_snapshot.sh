#!/usr/bin/env bash
# publicar_snapshot: publica no GitHub (repo PUBLICO; o Streamlit Cloud serve o app a partir dele) um
# SNAPSHOT de uma branch local, sem o historico interno e sem os arquivos internos, depois de uma
# trava que procura dado interno no que vai sair. O historico completo fica so no servidor interno.
#
# Uso (na raiz do repo do app):
#   bash publicar_snapshot/publicar_snapshot.sh [--simular] [--ramo <branch>] [--versao]
#     --simular  mostra o que mudaria no GitHub e nao envia nada
#     --ramo     branch local publicada na branch de MESMO nome no GitHub (padrao: RAMO_PADRAO do .conf)
# Configuracao: publicar_snapshot.conf na raiz do app (modelo: publicar_snapshot.conf.example desta pasta).
#
# ORIGEM: github.com/rodilpinto/nuati-framework, pasta publicar_snapshot/. Nao edite uma copia.
# Nasceu de checklist-conformidade/scripts/publicar_github.sh (@ 92ac158); mudancas no CHANGELOG.md.
set -euo pipefail

VERSAO="1.0.0"
CONF="publicar_snapshot.conf"

simular=""
ramo=""
while [ $# -gt 0 ]; do
  case "$1" in
    --simular) simular=1 ;;
    --ramo) ramo="${2:?--ramo precisa de uma branch}"; shift ;;
    --versao) echo "publicar_snapshot $VERSAO"; exit 0 ;;
    *) echo "Argumento desconhecido: $1" >&2; exit 2 ;;
  esac
  shift
done

if [ ! -f "$CONF" ]; then
  echo "Falta $CONF na raiz do repo (modelo: publicar_snapshot/publicar_snapshot.conf.example)." >&2
  exit 2
fi

# Padroes do .conf (ele pode sobrescrever qualquer um)
REMOTO="github"
RAMO_PADRAO="main"
EXCLUIR=()
TRAVA=()
TRAVA_EXCETO=()
# shellcheck source=/dev/null
source "./$CONF"
ramo="${ramo:-$RAMO_PADRAO}"
EXCLUIR+=("$CONF")   # o .conf lista padroes de dado interno: nunca vai junto

if ! git rev-parse -q --verify "$ramo^{commit}" >/dev/null; then
  echo "A branch local '$ramo' nao existe." >&2
  exit 2
fi

git fetch --quiet "$REMOTO"
indice=$(mktemp)
trap 'rm -f "$indice"' EXIT
GIT_INDEX_FILE="$indice" git read-tree "$ramo"
for caminho in "${EXCLUIR[@]}"; do
  GIT_INDEX_FILE="$indice" git rm -r --cached --quiet --ignore-unmatch -- "$caminho"
done
arvore=$(GIT_INDEX_FILE="$indice" git write-tree)

# Trava de seguranca: nenhum dado interno pode ir junto. Erro do git grep (status > 1) tambem aborta.
if [ ${#TRAVA[@]} -gt 0 ]; then
  padrao=$(IFS='|'; echo "${TRAVA[*]}")
  fora=()
  for caminho in ${TRAVA_EXCETO[@]+"${TRAVA_EXCETO[@]}"}; do
    fora+=(":(exclude)$caminho")
  done
  set +e
  git grep -n -E "$padrao" "$arvore" -- . ${fora[@]+"${fora[@]}"}
  status=$?
  set -e
  if [ "$status" -eq 0 ]; then
    echo "ABORTADO: dado interno encontrado no snapshot (acima). Tire-o do codigo ou ponha o arquivo em EXCLUIR." >&2
    exit 1
  elif [ "$status" -ne 1 ]; then
    echo "ABORTADO: a trava nao conseguiu rodar (git grep saiu com $status)." >&2
    exit 1
  fi
fi

# Base: a propria branch no GitHub; se nao existir, a RAMO_PADRAO de la; se nada existir, o primeiro snapshot.
if git rev-parse -q --verify "$REMOTO/$ramo" >/dev/null; then
  base="$REMOTO/$ramo"
elif git rev-parse -q --verify "$REMOTO/$RAMO_PADRAO" >/dev/null; then
  base="$REMOTO/$RAMO_PADRAO"
else
  base=""
fi

if [ "$base" = "$REMOTO/$ramo" ] && [ "$arvore" = "$(git rev-parse "$base^{tree}")" ]; then
  echo "GitHub ($ramo) ja esta atualizado."
  exit 0
fi

if [ -n "$simular" ]; then
  if [ -n "$base" ]; then
    echo "SIMULACAO: arquivos que mudariam em $REMOTO/$ramo (base $base; nada foi enviado):"
    git diff --stat "$base" "$arvore" | tail -25
  else
    echo "SIMULACAO: primeiro snapshot em $REMOTO/$ramo (nada foi enviado). Arquivos:"
    git ls-tree -r --name-only "$arvore"
  fi
  exit 0
fi

mensagem="Snapshot publico de $ramo @ $(git rev-parse --short "$ramo") ($(date +%F))"
if [ -n "$base" ]; then
  commit=$(git commit-tree "$arvore" -p "$base" -m "$mensagem")
else
  commit=$(git commit-tree "$arvore" -m "$mensagem")
fi
git push --quiet "$REMOTO" "$commit:refs/heads/$ramo"
echo "Publicado: $commit em $REMOTO/$ramo"
