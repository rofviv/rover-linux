Para poder conectarse desde una pc windows a la vpn estando en la red local, ejecutar el siguiente comando en la consola de windows como administrador:

```bash
route -p add 10.13.13.0 mask 255.255.255.0 192.168.18.100

route print
```


Instalacion de Speedify en windows robot:

Para verificar las rutas configuradas:

```bash
Get-NetIPConfiguration
```

En el archivo .conf de wireguard, actualizar la siguiente linea:

```bash
AllowedIPs = 0.0.0.0/0 -> AllowedIPs = 10.13.13.0/24
```

Ejecutar como administrador el siguiente comando:

```bash
route -p add 10.13.13.0 mask 255.255.255.0 10.13.13.8 if 14
route -p add 10.13.13.1 mask 255.255.255.255 10.13.13.8 if 14

```

Verificar conexion a internet despues de realizar las configuraciones.
Verificar hacer ping a 10.13.13.1.


IMPORTANTE: Actualizar el host de jetpack_api.py y colocar la ip de la vpn.
