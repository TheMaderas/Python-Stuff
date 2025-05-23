"""
Utility for getting information about local and external IP addresses.
This script displays information about the local machine's IP addresses.
"""
import socket
import requests
from datetime import datetime
import argparse

def get_local_ip():
    """
    Gets the local IP address of the machine.
    
    Returns:
        str: Local IP address
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip

def get_external_ip():
    """
    Gets the external (public) IP address of the machine.
    
    Returns:
        str: External IP address or error message
    """
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        return response.text
    except Exception as e:
        return f"Could not get external IP: {str(e)}"

def get_hostname():
    """
    Gets the hostname of the local machine.
    
    Returns:
        str: Hostname
    """
    return socket.gethostname()

def main():
    parser = argparse.ArgumentParser(description='IP Information Utility')
    parser.add_argument('--no-external', action='store_true', help='Do not check external IP')
    parser.add_argument('--details', action='store_true', help='Show additional details')
    
    args = parser.parse_args()
    
    hostname = get_hostname()
    local_ip = get_local_ip()
    
    print('\n' + '='*50)
    print(' NETWORK INFORMATION ')
    print('='*50)
    
    print(f'Hostname: {hostname}')
    print(f'Local IP: {local_ip}')
    
    if not args.no_external:
        external_ip = get_external_ip()
        print(f'External IP: {external_ip}')
    
    if args.details:
        print('-'*50)
        print(f'Check date and time: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
        
        try:
            print('All network interfaces:')
            for interface, addrs in socket.getaddrinfo(socket.gethostname(), None):
                print(f' - {addrs[4][0]} (Family: {interface})')
        except Exception:
            print('Could not list all network interfaces')
    
    print('='*50 + '\n')

if __name__ == "__main__":
    main()
