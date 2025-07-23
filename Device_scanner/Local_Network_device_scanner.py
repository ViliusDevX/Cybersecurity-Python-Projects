import ipaddress
import subprocess
import platform
import socket
import concurrent.futures
import threading
import queue
import psutil
import time
from tqdm import tqdm
from getmac import get_mac_address

def get_local_subnet():
    interfaces = psutil.net_if_addrs()
    private_prefixes = ("192.168.", "10.", "172.")
    for interface in interfaces.values():
        for addr in interface:
            if addr.family == socket.AF_INET and any(addr.address.startswith(p) for p in private_prefixes):
                ip = ipaddress.IPv4Address(addr.address)
                netmask = ipaddress.IPv4Address(addr.netmask)
                network = ipaddress.IPv4Network((int(ip) & int(netmask), addr.netmask), strict=False)
                return network
    return ipaddress.IPv4Network("127.0.0.1/32")

def scan_worker(ip_queue, results, progress):
    while not ip_queue.empty():
        ip = ip_queue.get()
        try:
            start_time = time.time()
            system = platform.system()
            cmd = ["ping", "-n", "1", "-w", "300", str(ip)] if system == "Windows" else ["ping", "-c", "1", "-W", "1", str(ip)]
            response = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if "TTL=" in response.stdout or "ttl=" in response.stdout:
                mac = get_mac_address(ip=str(ip)) or "Unknown"
                latency = round((time.time() - start_time) * 1000)
                results.append((str(ip), latency, mac))
        except Exception as e:
            pass
        finally:
            progress.update(1)
            ip_queue.task_done()

def main():
    subnet = get_local_subnet()
    print(f"🔍 Scanning subnet: {subnet} (local)")

    ip_queue = queue.Queue()
    results = []

    for ip in subnet.hosts():
        ip_queue.put(ip)

    num_threads = 50
    threads = []
    pbar = tqdm(total=ip_queue.qsize(), desc="🔍 Scanning", colour="green")

    for _ in range(num_threads):
        thread = threading.Thread(target=scan_worker, args=(ip_queue, results, pbar), daemon=True)
        thread.start()
        threads.append(thread)

    ip_queue.join()
    pbar.close()

    print("\nDevices found:")
    if results:
        for ip, latency, mac in results:
            print(f"✅ {ip} | 🕒 {latency}ms | 🖧 MAC: {mac}")
    else:
        print("❌ No devices found.")

if __name__ == "__main__":
    main()
