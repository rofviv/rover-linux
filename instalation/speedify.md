### Boding in ubuntu

- Install speedify
https://support.speedify.com/article/562-install-speedify-linux

- USB and Wlan set both primaries

- Connect to start ON
- Route mode UDP
- ByPass mode ON

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
