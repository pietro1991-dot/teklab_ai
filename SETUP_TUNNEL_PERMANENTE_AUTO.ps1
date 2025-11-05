# ==================================================
# TUNNEL PERMANENTE CLOUDFLARE - GUIDA STEP BY STEP
# ==================================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   SETUP TUNNEL PERMANENTE CLOUDFLARE" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# STEP 1: Verifica login
Write-Host "[1/5] Verifica autenticazione Cloudflare..." -ForegroundColor Yellow
if (Test-Path "$env:USERPROFILE\.cloudflared\cert.pem") {
    Write-Host "✅ Già autenticato" -ForegroundColor Green
} else {
    Write-Host "⚠️  Eseguo login (aprirà browser)..." -ForegroundColor Yellow
    & "$env:USERPROFILE\cloudflared.exe" tunnel login
    
    if (-not (Test-Path "$env:USERPROFILE\.cloudflared\cert.pem")) {
        Write-Host "❌ Login fallito. Verifica di aver completato setup Zero Trust su:" -ForegroundColor Red
        Write-Host "   https://one.dash.cloudflare.com/" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""

# STEP 2: Crea tunnel
Write-Host "[2/5] Creazione tunnel permanente 'teklab-backend'..." -ForegroundColor Yellow
$createOutput = & "$env:USERPROFILE\cloudflared.exe" tunnel create teklab-backend 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Errore creazione tunnel:" -ForegroundColor Red
    Write-Host $createOutput -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUZIONE: Vai su https://one.dash.cloudflare.com/ e completa setup Zero Trust (piano FREE)" -ForegroundColor Yellow
    exit 1
}

Write-Host $createOutput -ForegroundColor Gray
Write-Host "✅ Tunnel creato!" -ForegroundColor Green

# STEP 3: Estrai tunnel ID
Write-Host ""
Write-Host "[3/5] Estrazione Tunnel ID..." -ForegroundColor Yellow
$tunnelId = ($createOutput | Select-String -Pattern "([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})").Matches.Value

if (-not $tunnelId) {
    Write-Host "❌ Impossibile estrarre Tunnel ID" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Tunnel ID: $tunnelId" -ForegroundColor Green

# STEP 4: Crea config.yml
Write-Host ""
Write-Host "[4/5] Creazione config.yml..." -ForegroundColor Yellow

$configContent = @"
tunnel: $tunnelId
credentials-file: $env:USERPROFILE\.cloudflared\$tunnelId.json

ingress:
  - service: http://localhost:5000
"@

New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cloudflared" | Out-Null
$configContent | Out-File -Encoding UTF8 "$env:USERPROFILE\.cloudflared\config.yml"

Write-Host "✅ Config salvato in: $env:USERPROFILE\.cloudflared\config.yml" -ForegroundColor Green

# STEP 5: Mostra URL permanente
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   ✅ TUNNEL PERMANENTE CONFIGURATO!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "URL PERMANENTE (usa questo in config.js):" -ForegroundColor Yellow
Write-Host "https://$tunnelId.cfargotunnel.com" -ForegroundColor Green
Write-Host ""
Write-Host "OPPURE (formato alternativo):" -ForegroundColor Yellow
Write-Host "https://teklab-backend-$tunnelId.trycloudflare.com" -ForegroundColor Green
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# STEP 6: Chiedi se avviare
$avvia = Read-Host "Vuoi avviare il tunnel adesso? (s/n)"

if ($avvia -eq "s" -or $avvia -eq "S") {
    Write-Host ""
    Write-Host "[5/5] Avvio tunnel permanente..." -ForegroundColor Yellow
    Write-Host "NOTA: Questo terminale deve rimanere aperto!" -ForegroundColor Yellow
    Write-Host ""
    
    & "$env:USERPROFILE\cloudflared.exe" tunnel run teklab-backend
} else {
    Write-Host ""
    Write-Host "Per avviare il tunnel in futuro, esegui:" -ForegroundColor Yellow
    Write-Host "  cloudflared tunnel run teklab-backend" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Oppure usa lo script: START_TUNNEL_PERMANENTE.bat" -ForegroundColor Cyan
}
