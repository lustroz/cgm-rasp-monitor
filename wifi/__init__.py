import subprocess
import requests
import logging

logger = logging.getLogger('cgm')

def checkNetwork():
    url = 'https://www.google.com/'
    timeout = 5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except OSError:
        logger.info('sdf')
        return False

def getApList():
    output = subprocess.check_output('iw dev wlan0 scan | egrep "signal|SSID"', universal_newlines=True)
    logger.info(output)
    return output


def connect(ssid, password):
    subprocess.check_output('wpa_passphrase "'+ssid+'" '+password+' >> /etc/wpa_supplicant/wpa_supplicant.conf', universal_newlines=True)


