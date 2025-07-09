import argparse
import ipaddress
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the CLI tool.
    """
    parser = argparse.ArgumentParser(description="Network Calculator Tool - Calculates network address, broadcast address, usable host range, and total number of hosts.")
    parser.add_argument("ip_address", help="The IP address (e.g., 192.168.1.1)")
    parser.add_argument("cidr_mask", help="The CIDR mask (e.g., 24)", type=int)
    return parser

def calculate_network_info(ip_address, cidr_mask):
    """
    Calculates network information based on the given IP address and CIDR mask.

    Args:
        ip_address (str): The IP address.
        cidr_mask (int): The CIDR mask.

    Returns:
        dict: A dictionary containing the network address, broadcast address,
              first usable host, last usable host, and total number of hosts.
              Returns None if an error occurs.
    """
    try:
        # Input validation: Check if CIDR mask is valid
        if not 0 <= cidr_mask <= 32:
            raise ValueError("CIDR mask must be between 0 and 32.")

        network = ipaddress.ip_network(f"{ip_address}/{cidr_mask}", strict=False)

        network_address = str(network.network_address)
        broadcast_address = str(network.broadcast_address)

        # Calculate usable host range
        if network.num_addresses > 2:
            first_usable_host = str(list(network.hosts())[0])
            last_usable_host = str(list(network.hosts())[-1])
        else:
            first_usable_host = "N/A (Network too small)"
            last_usable_host = "N/A (Network too small)"

        total_hosts = network.num_addresses

        return {
            "network_address": network_address,
            "broadcast_address": broadcast_address,
            "first_usable_host": first_usable_host,
            "last_usable_host": last_usable_host,
            "total_hosts": total_hosts
        }
    except ValueError as e:
        logging.error(f"Invalid input: {e}")
        print(f"Error: {e}", file=sys.stderr)  # Print to stderr for error messages
        return None
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        return None

def main():
    """
    Main function to parse arguments, calculate network information, and print results.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    ip_address = args.ip_address
    cidr_mask = args.cidr_mask

    # Validate the IP address format before proceeding to the network calculation
    try:
        ipaddress.ip_address(ip_address)
    except ValueError as e:
        logging.error(f"Invalid IP address format: {e}")
        print(f"Error: Invalid IP address format: {e}", file=sys.stderr)
        sys.exit(1)  # Exit with a non-zero status code to indicate an error

    network_info = calculate_network_info(ip_address, cidr_mask)

    if network_info:
        print(f"Network Address:   {network_info['network_address']}")
        print(f"Broadcast Address: {network_info['broadcast_address']}")
        print(f"First Usable Host: {network_info['first_usable_host']}")
        print(f"Last Usable Host:  {network_info['last_usable_host']}")
        print(f"Total Hosts:       {network_info['total_hosts']}")
    else:
        # Error message already printed in calculate_network_info
        sys.exit(1)  # Exit with a non-zero status code if network_info is None

if __name__ == "__main__":
    # Usage Examples:
    # python main.py 192.168.1.0 24
    # python main.py 10.0.0.1 8
    # python main.py 172.16.0.5 16
    main()