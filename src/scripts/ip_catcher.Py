 #!/usr/bin/env python3
 
import subprocess

mac_addresses = {
    'AMY': 'e4:5f:01:db:df:74',
    'BOB': 'e4:5f:01:db:e0:47',
    'CAT': 'd8:3a:dd:81:b7:00'
}

def scan_network():
    try:
        scan_output = subprocess.check_output(['sudo', 'arp-scan', '--localnet'], text=True)
        return scan_output
    except subprocess.CalledProcessError as e:
        print(f"scan fail: {e}")
        return ""

def find_mac_in_scan(scan_results, macs):
    for name, mac in macs.items():
        found = False
        for line in scan_results.splitlines():
            if mac.lower() in line.lower():
                ip_address = line.split()[0]
                print(f"{name} ({mac}) IP: {ip_address}")
                found = True
                break
        if not found:
            print(f"{name} ({mac}) not found")

if __name__ == '__main__':
    scan_results = scan_network()
    if scan_results:
        find_mac_in_scan(scan_results, mac_addresses)
