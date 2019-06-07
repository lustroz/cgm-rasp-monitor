import subprocess
import requests
import logging
import sys
import os
import socket
import urllib

logger = logging.getLogger('cgm')

def checkNetwork():
    addr = subprocess.check_output(['hostname', '-I']).decode('utf-8')
    if len(addr) > 7:
        return True
    else:
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
    os.system('wpa_passphrase "'+ssid+'" "'+password+'" >> /etc/wpa_supplicant/wpa_supplicant.conf')
    os.system('systemctl daemon-reload')
    os.system('systemctl restart dhcpcd')


