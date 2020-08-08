#!/usr/bin/env python3
# pistream_client.py
# Allows client to connect to streaming device,
# select stream, view stream options, and add/delete stream options

import socket

HOST = 'pifour.local'
PORT = 12019

s = socket.socket()
s.connect((HOST, PORT))
print("Connected to:", (HOST, PORT))

try:
    command = input(" > ")
    s.sendall(command)
    
    response = s.recv(8)
    while "\n" not in data:
        response += s.recv(8)
    
finally:
    s.close()
