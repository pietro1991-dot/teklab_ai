# TUNNEL PERMANENTE SENZA DOMINIO PROPRIO
# =========================================
# URL finale: https://teklab-backend-TUNNEL_ID.cfargotunnel.com

# STEP 1: Crea account Cloudflare gratuito su browser
# Vai su: https://dash.cloudflare.com/sign-up
# - Click "Connect your website or app" 
# - Scegli piano FREE
# - Completa registrazione

# STEP 2: Login cloudflared
& "$env:USERPROFILE\cloudflared.exe" tunnel login
# → Apre browser, seleziona account appena creato

# STEP 3: Crea tunnel
& "$env:USERPROFILE\cloudflared.exe" tunnel create teklab-backend
# Output esempio:
#   Tunnel credentials written to: C:\Users\USERNAME\.cloudflared\UUID.json
#   Created tunnel teklab-backend with id UUID

# STEP 4: Copia TUNNEL_ID dall'output (UUID lungo)
$tunnelId = Read-Host "Incolla TUNNEL_ID qui"

# STEP 5: Crea config.yml
$configContent = @"
tunnel: $tunnelId
credentials-file: $env:USERPROFILE\.cloudflared\$tunnelId.json

ingress:
  - service: http://localhost:5000
"@

New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cloudflared" | Out-Null
$configContent | Out-File -Encoding UTF8 "$env:USERPROFILE\.cloudflared\config.yml"

Write-Host ""
Write-Host "✅ Configurazione completata!"
Write-Host ""
Write-Host "URL PERMANENTE sarà:"
Write-Host "https://teklab-backend-$tunnelId.cfargotunnel.com"
Write-Host ""
Write-Host "Avvio tunnel..."

# STEP 6: Avvia tunnel con config
& "$env:USERPROFILE\cloudflared.exe" tunnel run teklab-backend
