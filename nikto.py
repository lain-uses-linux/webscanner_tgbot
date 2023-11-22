
import os

def nikto_scan(target):
    scan_output = os.popen(f"./binaries/nikto -h {target}").read().strip()
    
    print(scan_output)
    return scan_output



