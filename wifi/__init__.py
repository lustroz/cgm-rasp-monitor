import subprocess
import requests
import logging
import sys

logger = logging.getLogger('cgm')

def checkNetwork():
    url = 'https://www.google.com/'
    timeout = 5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except OSError:
        return False

def getApList():
    output = subprocess.check_output(['iw', 'dev', 'wlan0', 'scan'])
    result = ''
    for line in output.decode('utf-8').split('\n'):
        if 'SSID' in line:
            if len(result) > 0: result += ';'
            result += line
    return result

def connect(ssid, password):
    subprocess.check_call('wpa_passphrase "'+ssid+'" '+password+' >> /etc/wpa_supplicant/wpa_supplicant.conf', universal_newlines=True)


