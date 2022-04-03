#! /usr/bin/env python3

# File client program
import os, socket, sys, re
sys.path.append("../lib")       # for params
import params

# Setting up vars for proxy
switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("\tCan't parse server:port from '%s'" % server)
    sys.exit(1)

# Creating socket and attemptin to connect to port
s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("\tCreating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print("\tAttempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print("\tError: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('\tCould not open socket.')
    sys.exit(1)

# Opening "output" file from archive.py and sending it to server
messageFile = "output"
messagefd = os.open(messageFile, os.O_RDONLY)
s.send(b'1')
subMessage = os.read(messagefd,1024)
while len(subMessage):
    bytesSent = s.send(subMessage)
    subMessage = os.read(messagefd, 1024)
os.close(messagefd)

# Closing output and receiving confirmation message from server
s.shutdown(socket.SHUT_WR)

while True:
    data = s.recv(1024).decode()
    print("\tReceived: '%s'" % data)
    if len(data) == 0:
        break
print("\tZero length read.  Closing.")
s.close()
