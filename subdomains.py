
import os

def subdomains_scan(target):
    scan_output = os.popen(f"python binaries/certsh.py -d {target}").read().strip()
    
    print(scan_output)
    return scan_output


