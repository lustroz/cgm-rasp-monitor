from bluetooth import *
import os
import logging
import wifi
import time
import setting

logger = logging.getLogger('cgm')

def handleData(clientSock, data, state):
    arr = data.split(b'::')
    if len(arr) < 1:
        return

    logger.info("received [%s]" % data)

    cmd = arr[0]
    if len(arr) > 1:
        param = arr[1]
    else:
        param = b''      

    logger.info("cmd %s" % cmd)

    if cmd == b'check':
        clientSock.send(b'check::' + b'pass' + b'\n')

    elif cmd == b'settings':
        result = setting.getCurrentText().encode('utf-8')
        clientSock.send(b'settings::' + result + b'\n')

    elif cmd == b'wifi_list':
        output = wifi.getApList().encode('utf-8')
        clientSock.send(b'wifi_list::' + output + b'\n')

    elif cmd == b'connect_wifi':
        state.setCmdState(state.BT_SetupWifi)
        phrase = param.split(b';')
        ssid = phrase[0].decode('utf-8')
        wifi.connect(ssid, phrase[1].decode('utf-8'))
        setting.setSSID(ssid)
        os.system('reboot')
    
    elif cmd == b'reboot':
        state.setCmdState(state.BT_Reboot)
        os.system('reboot')        

    elif cmd == b'source_change':
        state.setCmdState(state.BT_SourceChange)
        setting.setSourceType(param.decode('utf-8'))

    elif cmd == b'ns_set':
        state.setCmdState(state.BT_NightScout)
        setting.setNSAddress(param.decode('utf-8'))

    elif cmd == b'ds_set':
        state.setCmdState(state.BT_DexcomShare)
        phrase = param.split(b';')
        if len(phrase) < 2:
            return

        setting.setDSUsername(phrase[0].decode('utf-8'))
        setting.setDSPassword(phrase[1].decode('utf-8'))

    elif cmd == b'alarm_val':
        state.setCmdState(state.BT_AlarmValue)
        phrase = param.split(b';')
        if len(phrase) < 3:
            return
        setting.setAlarmValues(phrase[0].decode('utf-8'), phrase[1].decode('utf-8'), phrase[2].decode('utf-8'))

    elif cmd == b'tg_bot_token':
        state.setCmdState(state.BT_TGBotToken)
        setting.setTGBotToken(param.decode('utf-8'))

def listen(state, cond):
    uuid = "db9b08f1-8026-4477-98b8-a3555f801052"
    
    # os.system("echo 'discoverable on\nquit' | bluetoothctl")

    serverSock=BluetoothSocket(RFCOMM)
    serverSock.bind(('',PORT_ANY))
    serverSock.listen(1)

    port = serverSock.getsockname()[1]

    advertise_service(serverSock, "CgmMonitor", service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ])
    logger.info("Waiting for connection : channel %d" % port)
    
    clientSock, _ = serverSock.accept()
    logger.info("accepted")

    state.setCmdState(state.BT_Connected)

    while True:
        try:
            data = clientSock.recv(1024)
            if len(data) == 0: 
                continue
           
            handleData(clientSock, data, state)

            with cond:
                cond.notifyAll()

        except:
            logger.info("disconnected")
            clientSock.close()
            serverSock.close()
            state.setCmdState(state.Unknown)
            return
        
        time.sleep(1)

                                             
