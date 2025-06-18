# Configurar métricas para asegurar prioridad
# PARA EJECUTAR ESCRIBIR:
# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
# .\configurar-red-vpn.ps1

Set-NetIPInterface -InterfaceAlias "peer7" -InterfaceMetric 10
Set-NetIPInterface -InterfaceAlias "Conexión de área local" -InterfaceMetric 50

# Asegurar categoría de red privada para permitir tráfico
Set-NetConnectionProfile -InterfaceAlias "peer7" -NetworkCategory Private

# Rutas persistentes para la red VPN
route -p add 10.13.13.0 mask 255.255.255.0 10.13.13.8 if 14

# Permitir pings
Enable-NetFirewallRule -Name FPS-ICMP4-echo-request-In

# Permitir tráfico TCP hacia Flask (puerto 5000)
$rule = Get-NetFirewallRule -DisplayName "Flask TCP 5000 WireGuard" -ErrorAction SilentlyContinue
if (-not $rule) {
    New-NetFirewallRule -DisplayName "Flask TCP 5000 WireGuard" `
        -Direction Inbound `
        -LocalPort 5000 `
        -Protocol TCP `
        -Action Allow `
        -InterfaceAlias "peer7"
}

Write-Output "✔️ Configuración aplicada. Puedes hacer ping a 10.13.13.8 y acceder a Flask desde la VPN."
