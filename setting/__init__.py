import json
import logging
import os

logger = logging.getLogger('cgm')

def getCurrent():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'r') as f:
        config = json.load(f)
        ssid = config['ssid']
        sourceType = config['source_type']
        ns_addr = config['ns_addr']
        ds_addr = config['ds_user']
        ds_pass = config['ds_pass']
        lowAlarm = config['low_alarm']
        highAlarm = config['high_alarm']
        noSigAlarm = config['no_signal_alarm_min']
        return 'ssid={0};source={1};ns_addr={2};ds_user={3};ds_pass={4};low={5};high={6};no_sig={7}'.format(ssid, sourceType, ns_addr, ds_user, ds_pass, lowAlarm, highAlarm, noSigAlarm)

    return ''

def setSSID(ssid):
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        config = json.load(f)
        config['ssid'] = ssid

        with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'wt') as of:
            json.dump(config, of)

def getSourceType():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        config = json.load(f)
        return config['source_type']

    return 'nightscout'

def setSourceType(source):
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        config = json.load(f)
        config['source_type'] = source

        with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'wt') as of:
            json.dump(config, of)

def getNSAddress():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        config = json.load(f)
        return config['ns_addr']

    return ''

def setNSAddress(addr):
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        config = json.load(f)
        config['ns_addr'] = addr

        with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'wt') as of:
            json.dump(config, of)

def getDSUsername():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        config = json.load(f)
        return config['ds_user']

    return ''

def setDSUsername(username):
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        config = json.load(f)
        config['ds_user'] = username
        
        with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'wt') as of:
            json.dump(config, of)

def getDSPassword():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        config = json.load(f)
        return config['ds_pass']

    return ''

def setDSPassword(password):
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        config = json.load(f)
        config['ds_pass'] = password
        
        with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'wt') as of:
            json.dump(config, of)

def getLowAlarm():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        config = json.load(f)
        return config['low_alarm']

    return 80

def getHighAlarm():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        config = json.load(f)
        return config['high_alarm']

    return 170

def getNoSignalAlarm():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        config = json.load(f)
        return config['no_signal_alarm_min']

    return 15

