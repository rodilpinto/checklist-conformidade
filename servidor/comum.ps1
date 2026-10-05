# Funcoes usadas por instalar_tarefa.ps1 e atualizar.ps1 (carregado com ". comum.ps1").
# So ASCII neste arquivo: o PowerShell 5.1 le .ps1 sem BOM como ANSI.

$Raiz    = Split-Path -Parent $PSScriptRoot
$Venv    = Join-Path $Raiz ".venv"
$Python  = Join-Path $Venv "Scripts\python.exe"
$Iniciar = Join-Path $PSScriptRoot "iniciar.cmd"

function Falha($msg) {
    Write-Host "[ERRO] $msg" -ForegroundColor Red
    exit 1
}

function Ok($msg) { Write-Host "[OK] $msg" -ForegroundColor Green }

function Exigir-Admin {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    $admin = ([Security.Principal.WindowsPrincipal]$id).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $admin) {
        Falha "Rode como Administrador (botao direito no PowerShell > Executar como administrador)."
    }
}

# Processos escutando na porta: @{ Id; Linha } (Linha = linha de comando).
function Ouvintes-Da-Porta([int]$Porta) {
    $ids = Get-NetTCPConnection -LocalPort $Porta -State Listen -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($id in $ids) {
        $p = Get-CimInstance Win32_Process -Filter "ProcessId = $id" -ErrorAction SilentlyContinue
        [pscustomobject]@{ Id = $id; Linha = $(if ($p) { $p.CommandLine } else { "" }) }
    }
}

# Para a tarefa e encerra o Streamlit que sobrar na porta. Recusa matar outro programa.
function Parar-App([string]$NomeTarefa, [int]$Porta) {
    if (Get-ScheduledTask -TaskName $NomeTarefa -ErrorAction SilentlyContinue) {
        Stop-ScheduledTask -TaskName $NomeTarefa -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 2
    foreach ($o in Ouvintes-Da-Porta $Porta) {
        if ($o.Linha -match "streamlit" -and $o.Linha -match "--server\.port $Porta") {
            Stop-Process -Id $o.Id -Force -ErrorAction SilentlyContinue
        } else {
            Falha "A porta $Porta esta ocupada por outro programa (PID $($o.Id): $($o.Linha)). Escolha outra com -Porta."
        }
    }
    Start-Sleep -Seconds 2
}

# Espera o Streamlit responder em /_stcore/health. Devolve $true se respondeu.
function Esperar-App([int]$Porta, [int]$Segundos = 90) {
    $fim = (Get-Date).AddSeconds($Segundos)
    while ((Get-Date) -lt $fim) {
        try {
            $r = Invoke-WebRequest -Uri "http://localhost:$Porta/_stcore/health" -UseBasicParsing -TimeoutSec 5
            if ($r.Content -match "ok") { return $true }
        } catch { }
        Start-Sleep -Seconds 3
    }
    return $false
}

function Instalar-Dependencias {
    Write-Host "Instalando dependencias (requirements.txt)..."
    & $Python -m pip install --disable-pip-version-check -q -r (Join-Path $Raiz "requirements.txt")
    if ($LASTEXITCODE -ne 0) {
        Falha ("pip falhou (mensagem acima). Causas comuns: proxy (defina HTTPS_PROXY e rode de novo) " +
               "ou caminho longo demais, WinError 206 (clone numa pasta curta, como C:/apps/checklist-conformidade).")
    }
    Ok "dependencias instaladas"
}
