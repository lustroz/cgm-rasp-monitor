import json
import logging
import os

logger = logging.getLogger('cgm')

def getCurrent():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'r') as f:
        config = json.load(f)
        apName = config['ap_name']
        sourceType = config['source_type']
        addr = config['addr']
        password = config['pass']
        lowAlarm = config['low_alarm']
        highAlarm = config['high_alarm']
        noSigAlarm = config['no_signal_alarm_min']
        return 'ap={0};source={1};addr={2};pass={3};low={4};high={5};no_sig={6}'.format(apName, sourceType, addr, password, lowAlarm, highAlarm, noSigAlarm)

    return ''

