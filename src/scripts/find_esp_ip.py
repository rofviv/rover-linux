# pip install scapy
# pip install netifaces
# readlink -f $(which python3)
# sudo setcap cap_net_raw+eip /usr/bin/python3.10
# python3 find_esp_ip.py

import os
import netifaces
import ipaddress
from scapy.all import ARP, Ether, srp


PROJECT_ROOT = os.environ.get('PROJECT_ROOT', os.getcwd())
IP_RELAY_FILE = os.path.join(PROJECT_ROOT, 'status', 'ip_relay.txt')
relay_mac_prefixes = ["D8:BF:C0"]

def get_local_network():
    interfaces = netifaces.interfaces()
    for iface in interfaces:
        addrs = netifaces.ifaddresses(iface).get(netifaces.AF_INET)
        if addrs:
            for addr in addrs:
                ip = addr['addr']
                netmask = addr['netmask']
                print(f"IP: {ip}, Netmask: {netmask}")
                if ip.startswith("192.168"):
                    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                    return str(network)
    return None

def get_relay_ip():
    network_range = get_local_network()
    if not network_range:
        print("No se detectó una red 192.168.x.x activa.")
        return None
    else:
        print(f"Red detectada: {network_range}")

    print(f"Escaneando la red {network_range}...")

    arp_request = ARP(pdst=network_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp_request

    result = srp(packet, timeout=3, verbose=False)[0]

    for sent, received in result:
        mac = received.hwsrc.upper()
        ip = received.psrc
        if any(mac.startswith(prefix) for prefix in relay_mac_prefixes):
            return ip

    return None

relay_ip = get_relay_ip()

if relay_ip:
    with open(IP_RELAY_FILE, "w") as f:
        f.write(relay_ip)
    print(f"RELAY detectado en {relay_ip}. IP guardada en {IP_RELAY_FILE}")
else:
    print("No se detectó ningún RELAY en la red.")
