import subprocess
import urllib
import logging

logger = logging.getLogger('cgm')

def checkNetwork():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

def getApList():
    output = subprocess.check_output('iw dev wlan0 scan | egrep "signal|SSID"', universal_newlines=True)
    logger.info(output)
    return output


def connect(ssid, password):
    subprocess.check_output('wpa_passphrase "'+ssid+'" '+password+' >> /etc/wpa_supplicant/wpa_supplicant.conf', universal_newlines=True)


