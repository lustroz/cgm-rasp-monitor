from bluetooth import *
import os
import logging
import wifi

logger = logging.getLogger('cgm')

def handleData(clientSock, data):
    logger.info("received [%s]" % data)
    arr = data.split(':')
    if len(arr) < 2:
        return

    cmd = arr[0]
    param = arr[1]

    if cmd == 'wifi_list':
        output = wifi.getApList()
        clientSock.send(output)

    elif cmd == 'connect_wifi':
        wifi.connect(param)


def start():
    uuid = "db9b08f1-8026-4477-98b8-a3555f801052"
    
    os.system("echo 'discoverable on\nquit' | bluetoothctl")

    serverSock=BluetoothSocket(RFCOMM)
    serverSock.bind(('',PORT_ANY))
    serverSock.listen(1)

    port = serverSock.getsockname()[1]

    advertise_service(serverSock, "CgmMonitor", service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ])
    logger.info("Waiting for connection : channel %d" % port)
    
    clientSock, clientInfo = serverSock.accept()
    logger.info("accepted")

    while True:
        logger.info("Accepted connection from ", clientInfo)
        try:
            data = clientSock.recv(1024)
            if len(data) == 0: break
            handleData(data)

        except IOError:
            print("disconnected")
            clientSock.close()
            serverSock.close()
            break

        except KeyboardInterrupt:
            print("disconnected")
            clientSock.close()
            serverSock.close()
            break
                                             