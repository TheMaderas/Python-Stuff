"""
Utility for monitoring system resources.
This script allows monitoring CPU, memory, disk, and network in real-time.
"""
import psutil
import argparse
import time
import os
import datetime
import sys
import platform
from tabulate import tabulate
import socket

def get_size(bytes):
    """
    Converts bytes to a readable format (KB, MB, GB, etc.).
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} PB"

def get_cpu_info():
    """
    Gets CPU information.
    """
    cpu_info = {
        "usage": f"{psutil.cpu_percent()}%",
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "frequency": f"{psutil.cpu_freq().current:.2f} MHz" if psutil.cpu_freq() else "N/A"
    }
    
    per_cpu = psutil.cpu_percent(percpu=True)
    for i, percentage in enumerate(per_cpu):
        cpu_info[f"core_{i}"] = f"{percentage}%"
    
    return cpu_info

def get_memory_info():
    """
    Gets memory information.
    """
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    memory_info = {
        "total": get_size(mem.total),
        "available": get_size(mem.available),
        "used": get_size(mem.used),
        "percentage": f"{mem.percent}%",
        "swap_total": get_size(swap.total),
        "swap_free": get_size(swap.free),
        "swap_used": get_size(swap.used),
        "swap_percentage": f"{swap.percent}%"
    }
    
    return memory_info

def get_disk_info():
    """
    Gets disk information.
    """
    partitions = psutil.disk_partitions()
    disk_info = {}
    
    for i, partition in enumerate(partitions):
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            disk_info[f"partition_{i}_device"] = partition.device
            disk_info[f"partition_{i}_mountpoint"] = partition.mountpoint
            disk_info[f"partition_{i}_filesystem"] = partition.fstype
            disk_info[f"partition_{i}_total"] = get_size(partition_usage.total)
            disk_info[f"partition_{i}_used"] = get_size(partition_usage.used)
            disk_info[f"partition_{i}_free"] = get_size(partition_usage.free)
            disk_info[f"partition_{i}_percentage"] = f"{partition_usage.percent}%"
        except:
            continue
    
    io_counters = psutil.disk_io_counters()
    if io_counters:
        disk_info["io_read"] = get_size(io_counters.read_bytes)
        disk_info["io_written"] = get_size(io_counters.write_bytes)
    
    return disk_info

def get_network_info():
    """
    Gets network information.
    """
    net_io = psutil.net_io_counters()
    net_addrs = psutil.net_if_addrs()
    
    network_info = {
        "bytes_sent": get_size(net_io.bytes_sent),
        "bytes_received": get_size(net_io.bytes_recv),
        "packets_sent": net_io.packets_sent,
        "packets_received": net_io.packets_recv
    }
    
    for interface, addrs in net_addrs.items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                network_info[f"{interface}_mac"] = addr.address
            elif addr.family == socket.AF_INET:
                network_info[f"{interface}_ipv4"] = addr.address
            elif addr.family == socket.AF_INET6:
                network_info[f"{interface}_ipv6"] = addr.address
    
    return network_info

def get_process_info(sort_by="memory", top_n=5):
    """
    Gets information about running processes.
    
    Args:
        sort_by (str): Sorting criteria ("memory", "cpu", "name")
        top_n (int): Number of processes to show
    """
    processes = []
    
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent', 'pid', 'username']):
        try:
            info = proc.info
            cpu_val = info.get('cpu_percent') or 0.0
            mem_val = info.get('memory_percent') or 0.0
            processes.append({
                'pid': info.get('pid'),
                'name': info.get('name'),
                'cpu': cpu_val,
                'memory': mem_val,
                'user': info.get('username')
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if sort_by == "memory":
        processes.sort(key=lambda x: x['memory'], reverse=True)
    elif sort_by == "cpu":
        processes.sort(key=lambda x: x['cpu'], reverse=True)
    elif sort_by == "name":
        processes.sort(key=lambda x: x['name'] or "")
    
    return processes[:top_n]

def monitor_single():
    """
    Runs a single system resource check.
    """
    cpu = get_cpu_info()
    memory = get_memory_info()
    disk = get_disk_info()
    network = get_network_info()
    processes = get_process_info()

    print(f"\nDate and Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System: {platform.system()} {platform.release()} ({platform.machine()})")

    print("\n--- CPU ---")
    print(f"Total Usage: {cpu['usage']}")
    print(f"Physical Cores: {cpu['physical_cores']}")
    print(f"Total Cores: {cpu['total_cores']}")
    print(f"Frequency: {cpu['frequency']}")

    print("\n--- Memory ---")
    print(f"Total: {memory['total']}")
    print(f"Available: {memory['available']}")
    print(f"Used: {memory['used']} ({memory['percentage']})")

    print("\n--- Disk ---")
    for key, val in disk.items():
        print(f"{key.replace('_', ' ').title()}: {val}")

    print("\n--- Network ---")
    print(f"Bytes Sent: {network['bytes_sent']}")
    print(f"Bytes Received: {network['bytes_received']}")

    print("\n--- Top Processes by Memory ---")
    headers = ["PID", "Name", "CPU %", "Memory %", "User"]
    table = [[p['pid'], p['name'], f"{p['cpu']:.1f}%", f"{p['memory']:.1f}%", p['user']] for p in processes]
    print(tabulate(table, headers=headers))

def monitor_continuous(interval=1.0, duration=None):
    """
    Continuously monitors system resources.

    Args:
        interval (float): Seconds between updates
        duration (int): Total monitoring duration in seconds
    """
    try:
        count = 0
        start_time = time.time()
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            elapsed = time.time() - start_time
            print(f"System Monitor - Refresh every {interval}s | Elapsed: {int(elapsed)}s")

            cpu_percent = psutil.cpu_percent(interval=0)
            memory = psutil.virtual_memory()
            print("\nCPU: {0:.1f}% | Memory: {1:.1f}% | Time: {2}".format(cpu_percent, memory.percent, datetime.datetime.now().strftime('%H:%M:%S')))

            bar_len = 30
            cpu_bar = '█' * int(cpu_percent/100 * bar_len)
            print(f"CPU [{cpu_bar.ljust(bar_len)}] {cpu_percent:.1f}%")
            mem_bar = '█' * int(memory.percent/100 * bar_len)
            print(f"MEM [{mem_bar.ljust(bar_len)}] {memory.percent:.1f}%")

            processes = get_process_info(sort_by="cpu", top_n=10)
            headers = ["PID", "Name", "CPU %", "Memory %", "User"]
            table = [[p['pid'], p['name'][:20], f"{p['cpu']:.1f}%", f"{p['memory']:.1f}%", p['user'][:10]] for p in processes]
            print(tabulate(table, headers=headers))

            if count % 5 == 0:
                disk = psutil.disk_usage('/')
                print(f"\nDisk Usage: {get_size(disk.used)}/{get_size(disk.total)} ({disk.percent}%)")

            count += 1
            if duration and elapsed >= duration:
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

def main():
    parser = argparse.ArgumentParser(description='System Resource Monitor')
    parser.add_argument('-c', '--continuous', action='store_true',
                        help='Monitor continuously (refresh mode)')
    parser.add_argument('-i', '--interval', type=float, default=1.0,
                        help='Interval between updates in seconds')
    parser.add_argument('-d', '--duration', type=int,
                        help='Total monitoring duration in seconds')
    parser.add_argument('-o', '--output', type=str,
                        help='Save results to a file')
    
    args = parser.parse_args()
    
    print('\n' + '='*60)
    print(' SYSTEM RESOURCE MONITOR ')
    print('='*60)
    
    if args.output:
        original_stdout = sys.stdout
        try:
            sys.stdout = open(args.output, 'w')
        except Exception as e:
            print(f"Error opening output file: {str(e)}")
            return
    
    try:
        if args.continuous:
            monitor_continuous(args.interval, args.duration)
        else:
            monitor_single()
    finally:
        if args.output:
            sys.stdout.close()
            sys.stdout = original_stdout
            print(f"Results saved to: {args.output}")

if __name__ == "__main__":
    main()
