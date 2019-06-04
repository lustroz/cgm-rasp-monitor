from bluetooth import *
import os
import logging
import wifi
import time
import setting

logger = logging.getLogger('cgm')

def handleData(clientSock, data):
    logger.info("received [%s]" % data)

    arr = data.split(b':')
    if len(arr) < 1:
        return

    cmd = arr[0]

    count = arr[0].decode('utf-8')
    if count.isdigit():
        argc = int(count)
        if argc > 1:
            cmd = arr[1]
            param = arr[2:]            

    if cmd == b'settings':
        result = setting.getCurrent().encode('utf-8')
        clientSock.send(b'settings:' + result)

    if cmd == b'wifi_list':
        output = wifi.getApList().encode('utf-8')
        clientSock.send(b'wifi_list:' + output)

    elif cmd == b'connect_wifi':
        phrase = param.split(b';')
        wifi.connect(phrase[0], phrase[1])
    
    elif cmd == b'reboot':
        os.system('shutdown -r now')

    elif cmd == b'source_change':
        pass

    elif cmd == b'nightscout':
        pass

    elif cmd == b'dexcomshare':
        phrase = param.split(b';')
        pass

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

    state.setState(state.BluetoothConnected)

    while True:
        try:
            data = clientSock.recv(1024)
            if len(data) == 0: 
                continue
           
            handleData(clientSock, data)

            with cond:
                cond.notifyAll()

        except KeyboardInterrupt:
            logger.info("disconnected")
            clientSock.close()
            serverSock.close()
            return
        
        time.sleep(1)

    state.setState(state.Unknown)
                                             
