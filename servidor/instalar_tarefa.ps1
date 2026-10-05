# Instala o checklist-conformidade como tarefa agendada do Windows (sobe junto com o servidor).
# Rode UMA VEZ, como Administrador, da raiz do clone:
#   powershell -ExecutionPolicy Bypass -File servidor\instalar_tarefa.ps1 [-Porta 8401]
# Pode rodar de novo: refaz a tarefa sem duplicar. Receita completa: servidor\README.md.
# Modelo: instalar_servico.ps1 do pesquisa_diario (AppDOU).

param(
    [int]$Porta = 8401,
    [string]$NomeTarefa = "ChecklistConformidade"
)

. (Join-Path $PSScriptRoot "comum.ps1")

Exigir-Admin

# 1. Python 3.10+. O "python" da Microsoft Store e so um atalho e nao serve.
function Achar-Python {
    foreach ($cand in @(@("py", "-3"), @("python"))) {
        if (-not (Get-Command $cand[0] -ErrorAction SilentlyContinue)) { continue }
        $extra = @($cand | Select-Object -Skip 1)
        $v = & $cand[0] @extra -c "import sys; print('%d.%d' % sys.version_info[:2])" 2>$null
        if ($LASTEXITCODE -eq 0 -and "$v" -match '^3\.(\d+)$' -and [int]$Matches[1] -ge 10) {
            return ,$cand
        }
    }
    return $null
}

if (Test-Path $Python) {
    Ok "ambiente virtual ja existe (.venv)"
} else {
    $py = Achar-Python
    if (-not $py) {
        Falha "Python 3.10 ou mais novo nao encontrado. Instale de python.org (marque 'Add python.exe to PATH') e rode de novo."
    }
    Write-Host "Criando .venv com: $($py -join ' ')"
    $extra = @($py | Select-Object -Skip 1)
    & $py[0] @extra -m venv $Venv
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $Python)) { Falha "nao consegui criar o .venv" }
    Ok "ambiente virtual criado (.venv)"
}

# 2. Dependencias
Instalar-Dependencias

# 3. Configuracao: o .env nao vai para o git
if (-not (Test-Path (Join-Path $Raiz ".env"))) {
    Falha "Falta o .env na raiz do clone. Copie .env.example para .env, preencha (valores em _sessao\INTERNO.md) e rode de novo."
}
Ok ".env encontrado"

# 4. Tarefa agendada: sobe com o Windows, sem usuario logado, reinicia se cair
Parar-App $NomeTarefa $Porta
Unregister-ScheduledTask -TaskName $NomeTarefa -Confirm:$false -ErrorAction SilentlyContinue

$Action = New-ScheduledTaskAction `
    -Execute "cmd.exe" `
    -Argument "/c `"`"$Iniciar`" $Porta`"" `
    -WorkingDirectory $Raiz

$Trigger = New-ScheduledTaskTrigger -AtStartup

$Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 0) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew

$Principal = New-ScheduledTaskPrincipal `
    -UserId "SYSTEM" `
    -LogonType ServiceAccount `
    -RunLevel Highest

Register-ScheduledTask `
    -TaskName $NomeTarefa `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "checklist-conformidade (Streamlit) na porta $Porta. Pasta: $Raiz" `
    -ErrorAction Stop | Out-Null
Ok "tarefa '$NomeTarefa' registrada"

# 5. Firewall do Windows (a liberacao da rede e outra camada)
$Regra = "checklist-conformidade (TCP $Porta)"
if (-not (Get-NetFirewallRule -DisplayName $Regra -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -DisplayName $Regra -Direction Inbound -Protocol TCP -LocalPort $Porta -Action Allow | Out-Null
    Ok "regra de firewall criada: $Regra"
} else {
    Ok "regra de firewall ja existe: $Regra"
}

# 6. Sobe agora e confere
Start-ScheduledTask -TaskName $NomeTarefa
Write-Host "Aguardando o app responder na porta $Porta..."
if (Esperar-App $Porta) {
    Ok "app no ar: http://$($env:COMPUTERNAME):$Porta/"
} else {
    Falha "o app nao respondeu em 90 s. Veja logs\app.log."
}
