# network_topology_mapper/src/main/python/network_mapper/network_discovery.py

import logging
from scapy.all import ARP, Ether, srp
from tqdm import tqdm  # Import tqdm for the progress bar
import ipaddress
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def discover_devices(ip_range, depth=1, exclude_networks=None, timeout=3, verbose=False):
    """
    Discover devices on the network using ARP requests.

    Args:
        ip_range (str): The IP range to scan, e.g., "192.168.1.1/24".
        depth (int): The depth of network crawling or hops.
        exclude_networks (list): List of networks to exclude from scanning, it could be an entire subnet.
        timeout (int): Timeout for ARP requests.
        verbose (bool): Whether to print additional information.

    Returns:
        list: List of discovered devices with their IP and MAC addresses.
    """
    discovered_devices = []

    start_time = time.time()

    # Convert the IP range to a network
    network = ipaddress.ip_network(ip_range, strict=False)

    # Create an ARP request packet for each IP in the network
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(network))

    try:
        # Send and receive ARP requests using scapy
        result = srp(arp_request, timeout=timeout, verbose=False)[0]

        # Process the received responses and update the progress bar in real-time
        total_ips = len(result)
        with tqdm(total=total_ips, desc="Discovering Devices", unit="IP", dynamic_ncols=True) as progress_bar:
            for sent, received in result:
                ip = received.psrc
                mac = received.hwsrc

                # Check if the IP is not in the excluded networks
                if not any(ipaddress.ip_address(ip) in ipaddress.ip_network(exclude) for exclude in (exclude_networks or [])):
                    discovered_devices.append({'ip': ip, 'mac': mac})

                # Update the progress bar
                progress_bar.update(1)
                # Log loading progress in real-time
                if verbose:
                    logger.info(f"Loading: {progress_bar.n}/{progress_bar.total} IPs processed")

        end_time = time.time()
        elapsed_time = end_time - start_time

        logger.info("Device discovery completed successfully.")
        logger.info(f"Total Time: {elapsed_time:.2f} seconds")
        logger.info(f"Number of Hosts Discovered: {len(discovered_devices)}")

        return discovered_devices

    except Exception as e:
        logger.error(f"Error during device discovery: {e}")
        return []


# Example usage:
# from network_mapper.network_discovery import discover_devices
# devices = discover_devices("192.168.1.1/24", depth=1, timeout=3, verbose=True)
# for device in devices:
#     print(f"IP: {device['ip']}, MAC: {device['mac']}")
