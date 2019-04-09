import json
import logging

logger = logging.getLogger('cgm')

def getCurrent():
    with open('config.json', 'r') as f:
        config = json.load(f)
        apName = config['ap_name']
        sourceType = config['source_type']
        addr = config['addr']
        password = config['pass']
        lowAlarm = config['low_alarm']
        highAlarm = config['high_alarm']
        noSigAlarm = config['no_signal_alarm_min']
        return b'ap=%s;source=%s;addr=%s;pass=%s;low=%s;high=%s;no_sig=%s'.format(apName, sourceType, addr, password, lowAlaram, highAlarm, noSignalAlarm)

    return b''

