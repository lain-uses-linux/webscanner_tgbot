

import os

def dirbuster_scan(target):
    scan_output = os.popen(f"python binaries/web_crawler.py -d {target} -l 1").read().strip()
    scan_output = scan_output.split('\n')
    scan_result = ''
    print(scan_output)
    for i in scan_output:
        
        scan_result += i.split()[1] + "\n"
        

    print(scan_result)
    return scan_result



