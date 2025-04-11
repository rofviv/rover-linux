### Boding in ubuntu

- Install speedify
https://support.speedify.com/article/562-install-speedify-linux

- USB and Wlan set both primaries

- Connect at startup ON
- Transport mode UDP
- ByPass mode ON
- login to speedify, patiouser@***** : Pass****

- Add sudo permission to speedify (change tu_usuario to your user) add to end of file

```bash
sudo visudo
tu_usuario ALL=(ALL) NOPASSWD: /sbin/ip route add 192.168.18.0/24 dev wg0, /sbin/ip route add 10.13.13.0/24 dev wg0
```

- Add routes to launcher rover or file add_ip_route.sh

```bash
sudo ip route add 192.168.18.0/24 dev wg0
sudo ip route add 10.13.13.0/24 dev wg0
```




DEPRECATED
- Config Wireguard client
```bash
sudo vim /etc/wireguard/wg0.conf
AllowedIPs = 10.13.13.0/24

sudo wg-quick down wg0
sudo wg-quick up wg0
```

- Check route vpn
```bash
ip route get 10.13.13.1
ping 10.13.13.1
```
