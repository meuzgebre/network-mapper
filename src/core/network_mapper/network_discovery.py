# network_discovery.py

from scapy.all import ARP, Ether, srp
import ipaddress

def discover_devices(ip_range, depth=1, exclude_networks=None):
    discovered_devices = []

    # Convert the IP range to a network
    network = ipaddress.ip_network(ip_range, strict=False)

    # Create an ARP request packet for each IP in the network
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(network))

    # Send and receive ARP requests using scapy
    result = srp(arp_request, timeout=3, verbose=False)[0]

    # Process the received responses
    for sent, received in result:
        ip = received.psrc
        mac = received.hwsrc

        # Check if the IP is not in the excluded networks
        if not any(ipaddress.ip_address(ip) in ipaddress.ip_network(exclude) for exclude in (exclude_networks or [])):
            discovered_devices.append({'ip': ip, 'mac': mac})

    return discovered_devices

if __name__ == "__main__":
    # Example usage
    ip_range = "192.168.1.1/24"
    depth = 2
    exclude_networks = ["192.168.1.0/24"]

    devices = discover_devices(ip_range, depth, exclude_networks)
    for device in devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}")
