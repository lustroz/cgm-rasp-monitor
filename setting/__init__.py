import json
import logging
import os

logger = logging.getLogger('cgm')

def getCurrent():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'rt') as f:
        return json.load(f)
    return None

def save(config):
    with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json', 'wt') as of:
        json.dump(config, of)      

def getCurrentText():
    config = getCurrent()
    if config == None:
        return ''

    ssid = config['ssid']
    sourceType = config['source_type']
    ns_addr = config['ns_addr']
    ds_user = config['ds_user']
    ds_pass = config['ds_pass']
    lowAlarm = config['low_alarm']
    highAlarm = config['high_alarm']
    noSigAlarm = config['no_signal_alarm_min']
    tgBotToken = config['tg_bot_token']
    tgNormalPeriod = config['tg_normal_period']
    tgUrgentPeriod = config['tg_urgent_period']

    text = 'ssid={0};source={1};ns_addr={2};ds_user={3};ds_pass={4};low={5};high={6};no_sig={7};tg_bot_token={8};tg_normal_period={9};tg_urgent_period={10}'
    return text.format(ssid, sourceType, ns_addr, ds_user, ds_pass, lowAlarm, highAlarm, noSigAlarm, tgBotToken, tgNormalPeriod, tgUrgentPeriod)

def setSSID(ssid):
    config = getCurrent()
    config['ssid'] = ssid
    save(config)              

def getSourceType():
    config = getCurrent()
    return config['source_type']

def setSourceType(source):
    config = getCurrent()
    config['source_type'] = source
    save(config)

def setNSAddress(addr):
    config = getCurrent()
    config['ns_addr'] = addr
    save(config)

def setDSUsername(username):
    config = getCurrent()
    config['ds_user'] = username
    save(config)

def setDSPassword(password):
    config = getCurrent()
    config['ds_pass'] = password
    save(config)

def setAlarmValues(low, high, noSignal):
    config = getCurrent()
    config['low_alarm'] = low
    config['high_alarm'] = high
    config['no_signal_alarm_min'] = noSignal
    save(config)

def setTGBotToken(token):
    config = getCurrent()
    config['tg_bot_token'] = token
    save(config)

def setTGNormalPeriod(period):
    config = getCurrent()
    config['tg_normal_period'] = period
    save(config)

def setTGUrgentPeriod(period):
    config = getCurrent()
    config['tg_urgent_period'] = period
    save(config)

def setTGChatId(chatId):
    config = getCurrent()
    config['tg_chat_id'] = chatId
    save(config)

