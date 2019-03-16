from bluetooth import *
import os

async def listen():
    uuid = "db9b08f1-8026-4477-98b8-a3555f801052"
    
    os.system("echo 'discoverable on\nquit' | bluetoothctl")

    serverSock=BluetoothSocket(RFCOMM)
    serverSock.bind(('',PORT_ANY))
    serverSock.listen(1)

    port = serverSock.getsockname()[1]

    advertise_service(serverSock, "CgmMonitor", service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ])
    print("Waiting for connection : channel %d" % port)
    
    clientSock, clientInfo = serverSock.accept()
    print("accepted")

    while True:
        print("Accepted connection from ", clientInfo)
        try:
            data = clientSock.recv(1024)
            if len(data) == 0: break
            print("received [%s]" % data)
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
                                             
