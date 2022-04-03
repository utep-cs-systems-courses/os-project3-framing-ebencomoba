#! /usr/bin/env python3

# File transfer server program

import socket, sys, os, re
sys.path.append("../lib")       # for params
import params, threading

def stringMessage_handler(conn):
    sendMsg = ("String received").encode()
    conn.send(sendMsg)
    strMessage = ''
    while True:
        data = conn.recv(1024).decode()
        strMessage += data
        if len(data) == 0:
            print("\tZero length read.")
            break
    print("\tMessage received: '%s'" % strMessage)

def fileTransfer_handler(conn):
    sendMsg = ("Files received").encode()
    conn.send(sendMsg)
    print("\tFiles received.")
    # While we still have files
    while True:
        titleSize = conn.recv(8).decode()
        if len(titleSize) == 0:
            print("\tEnd of file(s).")
            break
        fileName = conn.recv(int(titleSize)).decode()
        contentsSize = int(conn.recv(28).decode())
        with open(fileName, 'w') as outFile:
            while contentsSize:
                streamSize = min(1024, contentsSize)
                data = conn.recv(streamSize).decode()
                outFile.write(data)
                contentsSize -= len(data)

def request_handler(conn):
    if os.fork() == 0:
        print('\tConnected by', addr)
        contentType = int(conn.recv(1).decode())
        if contentType == 0:
            stringMessage_handler(conn)
        else:
            fileTransfer_handler(conn)
        conn.shutdown(socket.SHUT_WR)

# Declaring vars for proxy
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

# Creating socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(5)              # allow five outstanding requests
# s is a factory for connected sockets

while True:
    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    request_handler(conn)
    thread = threading.Thread(target=request_handler, args=(conn,))
    thread.start()
    
#conn.shutdown(socket.SHUT_WR)
#conn.close()
