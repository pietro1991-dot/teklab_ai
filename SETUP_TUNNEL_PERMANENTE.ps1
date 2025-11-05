# GUIDA TUNNEL PERMANENTE CON DOMINIO
# ======================================

# PREREQUISITO: Dominio aggiunto a Cloudflare
# 1. Vai su https://dash.cloudflare.com
# 2. Click "Add a Site" → Inserisci dominio → Segui wizard
# 3. Cambia nameserver presso registrar dominio

# STEP 1: Login (già fatto)
# & "$env:USERPROFILE\cloudflared.exe" tunnel login

# STEP 2: Crea tunnel permanente
& "$env:USERPROFILE\cloudflared.exe" tunnel create teklab-backend

# STEP 3: Annota TUNNEL_ID dall'output (es. a1b2c3d4-e5f6-...)

# STEP 4: Configura DNS (sostituisci TUNNEL_ID e TUODOMINIO.com)
& "$env:USERPROFILE\cloudflared.exe" tunnel route dns teklab-backend chatbot.TUODOMINIO.com

# STEP 5: Crea file config.yml
$tunnelId = "TUNNEL_ID_QUI"  # ← Sostituisci con UUID del tunnel
$configContent = @"
tunnel: $tunnelId
credentials-file: $env:USERPROFILE\.cloudflared\$tunnelId.json

ingress:
  - hostname: chatbot.TUODOMINIO.com
    service: http://localhost:5000
  - service: http_status:404
"@

New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cloudflared" | Out-Null
$configContent | Out-File -Encoding UTF8 "$env:USERPROFILE\.cloudflared\config.yml"

# STEP 6: Avvia tunnel (URL FISSO: https://chatbot.TUODOMINIO.com)
& "$env:USERPROFILE\cloudflared.exe" tunnel run teklab-backend
