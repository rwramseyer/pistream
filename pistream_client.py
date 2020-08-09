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
    while True:
        command = input(" > ") + "\n"
        s.sendall(command.encode())
        response = s.recv(1024)
        if response:
            print(response.decode())
        else:
            break

finally:
    s.close()
