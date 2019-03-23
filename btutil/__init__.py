from bluetooth import *
import os
import logging
import wifi
import time

logger = logging.getLogger('cgm')

def handleData(clientSock, data):
    logger.info("received [%s]" % data)
    arr = data.split(b':')
    if len(arr) < 2:
        return

    cmd = arr[0]
    param = arr[1]

    if cmd == b'wifi_list':
        output = wifi.getApList()
        clientSock.send(output)

    elif cmd == b'connect_wifi':
        phrase = param.split(b';')
        wifi.connect(phrase[0], phrase[1])


def listen(state):
    uuid = "db9b08f1-8026-4477-98b8-a3555f801052"
    
    # os.system("echo 'discoverable on\nquit' | bluetoothctl")

    serverSock=BluetoothSocket(RFCOMM)
    serverSock.bind(('',PORT_ANY))
    serverSock.listen(1)

    port = serverSock.getsockname()[1]

    advertise_service(serverSock, "CgmMonitor", service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ])
    logger.info("Waiting for connection : channel %d" % port)
    
    clientSock, clientInfo = serverSock.accept()
    logger.info("accepted")

    while True:
        try:
            data = clientSock.recv(1024)
            if len(data) == 0: continue
            state.setState(state.BluetoothCommand)
            handleData(clientSock, data)

        except IOError:
            print("disconnected")
            clientSock.close()
            serverSock.close()
            return

        except KeyboardInterrupt:
            print("disconnected")
            clientSock.close()
            serverSock.close()
            return
        
        time.sleep(1)
                                             
