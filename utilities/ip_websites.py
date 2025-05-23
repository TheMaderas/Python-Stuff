"""
Utility for getting information about website IP addresses.
This script allows discovering the IP address of a domain and getting additional information.
"""
import socket
import argparse
import time
import subprocess
import platform

def get_domain_ip(domain):
    """
    Gets the IP address associated with a domain name.
    
    Args:
        domain (str): Domain name to query
        
    Returns:
        str: IP address or error message
    """
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return "Could not resolve the address"
    except Exception as e:
        return f"Error: {str(e)}"

def get_domain_info(domain):
    """
    Gets more detailed information about a domain.
    
    Args:
        domain (str): Domain name to query
        
    Returns:
        dict: Dictionary with domain information
    """
    info = {"domain": domain}
    
    try:
        info["ip"] = socket.gethostbyname(domain)
        
        try:
            host_info = socket.gethostbyname_ex(domain)
            info["aliases"] = host_info[1]
            info["ips"] = host_info[2]
        except:
            info["aliases"] = []
            info["ips"] = [info["ip"]]
            
        try:
            s = socket.create_connection((domain, 80), timeout=2)
            info["can_connect"] = True
            info["local_endpoint"] = s.getsockname()
            info["remote_endpoint"] = s.getpeername()
            s.close()
        except:
            info["can_connect"] = False
            
        return info
    except Exception as e:
        return {"domain": domain, "error": str(e)}

def ping_domain(domain, count=4):
    """
    Executes a ping to the specified domain.
    
    Args:
        domain (str): Domain name to query
        count (int): Number of packets to send
        
    Returns:
        str: Ping result
    """
    system = platform.system().lower()
    
    if system == "windows":
        command = ["ping", "-n", str(count), domain]
    else:
        command = ["ping", "-c", str(count), domain]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Ping timed out - host may be unreachable"
    except Exception as e:
        return f"Error executing ping: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description='Website IP Checker')
    parser.add_argument('domain', type=str, nargs='?', default='google.com', 
                        help='Domain to check (default: google.com)')
    parser.add_argument('--info', action='store_true', help='Show detailed information')
    parser.add_argument('--ping', action='store_true', help='Execute ping to the domain')
    parser.add_argument('--ping-count', type=int, default=4, help='Number of ping packets (default: 4)')
    
    args = parser.parse_args()
    
    print('\n' + '='*60)
    print(f' IP CHECKER FOR: {args.domain} ')
    print('='*60)
    
    ip = get_domain_ip(args.domain)
    print(f'Host: {args.domain}')
    print(f'IP: {ip}')
    
    if args.info:
        print('\n' + '-'*60)
        print(' DETAILED INFORMATION ')
        print('-'*60)
        
        info = get_domain_info(args.domain)
        
        if "error" in info:
            print(f"Error getting detailed information: {info['error']}")
        else:
            if info.get("aliases"):
                print(f"Aliases: {', '.join(info['aliases']) or 'None'}")
            
            if info.get("ips") and len(info["ips"]) > 1:
                print(f"All IPs: {', '.join(info['ips'])}")
            
            print(f"Can connect: {'Yes' if info.get('can_connect') else 'No'}")
            
            if info.get("can_connect"):
                print(f"Local endpoint: {info.get('local_endpoint')}")
                print(f"Remote endpoint: {info.get('remote_endpoint')}")
    
    if args.ping:
        print('\n' + '-'*60)
        print(' PING RESULT ')
        print('-'*60)
        
        ping_result = ping_domain(args.domain, args.ping_count)
        print(ping_result)
    
    print('='*60 + '\n')

if __name__ == "__main__":
    main()