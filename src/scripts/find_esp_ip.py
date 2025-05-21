# readlink -f $(which python3)
# sudo setcap cap_net_raw+eip /usr/bin/python3.10

import os
import netifaces
import ipaddress
from scapy.all import ARP, Ether, srp, conf

PROJECT_ROOT = os.environ.get('PROJECT_ROOT', os.getcwd())
IP_RELAY_FILE = os.path.join(PROJECT_ROOT, 'status', 'ip_relay.txt')
relay_mac_prefixes = ["D8:13:2A"]

def get_local_networks_with_interfaces():
    """Devuelve una lista de tuplas (interfaz, red IPv4 192.168.x.x)."""
    networks = []
    interfaces = netifaces.interfaces()
    for iface in interfaces:
        addrs = netifaces.ifaddresses(iface).get(netifaces.AF_INET)
        if addrs:
            for addr in addrs:
                ip = addr['addr']
                netmask = addr['netmask']
                if ip.startswith("192.168"):
                    network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
                    networks.append((iface, str(network)))
    return networks

def scan_network_for_relay(iface, network_range):
    """Escanea la red desde una interfaz específica."""
    print(f"Escaneando la red {network_range} desde la interfaz {iface}...")

    conf.iface = iface  # usar interfaz específica
    arp_request = ARP(pdst=network_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp_request

    result = srp(packet, timeout=3, verbose=False)[0]

    for sent, received in result:
        mac = received.hwsrc.upper()
        ip = received.psrc
        print(f"Dispositivo detectado: IP={ip}, MAC={mac}")
        if any(mac.startswith(prefix) for prefix in relay_mac_prefixes):
            return ip
    return None

def get_relay_ip():
    networks = get_local_networks_with_interfaces()
    if not networks:
        print("No se detectaron redes 192.168.x.x activas.")
        return None

    for iface, network in networks:
        ip = scan_network_for_relay(iface, network)
        if ip:
            return ip
    return None

relay_ip = get_relay_ip()

if relay_ip:
    os.makedirs(os.path.dirname(IP_RELAY_FILE), exist_ok=True)
    with open(IP_RELAY_FILE, "w") as f:
        f.write(relay_ip)
    print(f"RELAY detectado en {relay_ip}. IP guardada en {IP_RELAY_FILE}")
else:
    print("No se detectó ningún RELAY en las redes disponibles.")
