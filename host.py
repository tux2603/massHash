import select
import socket
import time

host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host.bind(("", 1337))
host.listen(10)

maxZeros = 0

try:
    while 1:
        r, w, e = select.select([host], [], [], 1.0)
        if r:
            channel, info = host.accept()
            data = channel.recv(4096).decode('utf-8')
            typeCode = data[0]
            message = data[1:]

            if typeCode == 'z':
                if int(message) > maxZeros:
                    print('-' * 20 + ' NEW MAX ' + '-' * 20)
                    maxZeros = int(message)

            elif typeCode == 'k':
                messageParts = message.split()
                if int(messageParts[0]) >= maxZeros:
                    print(f'{messageParts[1]}: {messageParts[2]}    ({messageParts[0]})')

            channel.send(str(maxZeros).encode('utf-8')) # send timestamp
            channel.close() # disconnect
        
except:
    host.close()
    print("Exiting")
    exit(1)