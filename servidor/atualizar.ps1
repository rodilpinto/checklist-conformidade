# Atualiza o app no servidor: git pull, dependencias e reinicio da tarefa.
# Rode como Administrador, da raiz do clone, sempre que houver versao nova no Gitea:
#   powershell -ExecutionPolicy Bypass -File servidor\atualizar.ps1 [-Porta 8401]

param(
    [int]$Porta = 8401,
    [string]$NomeTarefa = "ChecklistConformidade"
)

. (Join-Path $PSScriptRoot "comum.ps1")

Exigir-Admin
if (-not (Get-ScheduledTask -TaskName $NomeTarefa -ErrorAction SilentlyContinue)) {
    Falha "A tarefa '$NomeTarefa' nao existe. Rode antes servidor\instalar_tarefa.ps1."
}

Set-Location $Raiz

# 1. Codigo novo. Alteracao local em arquivo versionado bloquearia o pull: avisa em vez de descartar.
$sujos = git status --porcelain --untracked-files=no
if ($sujos) {
    Falha "Ha alteracoes locais em arquivos versionados (git status). Resolva antes de atualizar:`n$sujos"
}
$antes = git rev-parse --short HEAD
git pull --ff-only
if ($LASTEXITCODE -ne 0) { Falha "git pull falhou (veja a mensagem acima). Nada foi reiniciado." }
$depois = git rev-parse --short HEAD

if ($antes -eq $depois) {
    Ok "ja estava na versao mais nova ($depois); reiniciando mesmo assim"
} else {
    Ok "codigo atualizado: $antes -> $depois"
    git log --oneline "$antes..$depois"
}

# 2. Dependencias (rapido quando nada mudou)
Instalar-Dependencias

# 3. Reinicio
Parar-App $NomeTarefa $Porta
Start-ScheduledTask -TaskName $NomeTarefa
Write-Host "Aguardando o app responder na porta $Porta..."
if (Esperar-App $Porta) {
    Ok "app no ar: http://$($env:COMPUTERNAME):$Porta/ (versao $depois)"
} else {
    Falha "o app nao respondeu em 90 s. Veja logs\app.log."
}
