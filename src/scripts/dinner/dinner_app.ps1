$AppID = "com.nexus.dinner_fxkeb4dgdm144!dinnerapp"
$TaskName = "Iniciar Dinner App"

$Action = New-ScheduledTaskAction -Execute "explorer.exe" -Argument "shell:AppsFolder\$AppID"
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

Register-ScheduledTask -TaskName $TaskName `
  -Action $Action `
  -Trigger $Trigger `
  -Principal $Principal `
  -Description "Inicia automáticamente la app Dinner instalada con MSIX al iniciar sesión" `
  -Force


# Powershell administrator
# Set-ExecutionPolicy RemoteSigned -Scope Process
# .\dinner_app.ps1
