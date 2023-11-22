

import os

def wappalyzer_scan(target):
    scan_output = os.popen(f"./binaries/wappalyzer --target {target} --disable-ssl").read().strip()
    scan_result = ''
    for i in scan_output.split('\n'):
        scan_result += i.split(':')[0] + '\n'
    print(scan_result)
    return scan_result



