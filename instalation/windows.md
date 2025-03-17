Para poder conectarse desde una pc windows a la vpn estando en la red local, ejecutar el siguiente comando en la consola de windows como administrador:

```bash
route -p add 10.13.13.0 mask 255.255.255.0 192.168.18.100

route print
```
