#! /usr/bin/env python3

# Echo server program

import socket, sys, re
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framingServer"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets


conn, addr = s.accept()  # wait until incoming connection request (and accept it)
print('\tConnected by', addr)
# If the message is a string
contentType = int(conn.recv(1).decode())
if contentType == 0:
    sendMsg = ("String received").encode()
    conn.send(sendMsg)
    print("\tMessage received: ")
    while 1:
        data = conn.recv(1024).decode()
        if len(data) == 0:
            print("\tZero length read.")
            break
        print(data)
# If the message are files
else:
    sendMsg = ("Files received").encode()
    conn.send(sendMsg)
    print("\tFiles received.")
    # While we still have files
    while 1:
        titleSize = conn.recv(8).decode()
        if len(titleSize) == 0:
            print("\tEnd of file.")
            break
        fileName = conn.recv(int(titleSize)).decode()
        contentsSize = int(conn.recv(28).decode())
        with open(fileName, 'w') as outFile:
            while contentsSize:
                streamSize = min(1024, contentsSize)
                data = conn.recv(streamSize).decode()
                outFile.write(data)
                contentsSize -= len(data)
conn.shutdown(socket.SHUT_WR)
conn.close()
