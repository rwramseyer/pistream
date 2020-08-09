#!/usr/bin/env python3
# pistream_server.py
# This program runs on the pi and displays available
# streams and allows stream selection

import socket
import csv
import subprocess

STREAM_FILE = "stream_options.csv"
DEBUG = False 

def change_stream(stream_id):
    stream = get_current_streams()[stream_id]
        
    print("changing stream to", stream)
    stream_url = stream[1]
    
    # terminate old stream_process
    global stream_process
    if stream_process:
        stream_process.terminate()

    # create new process
    if DEBUG:
        process = subprocess.Popen(["chromium-browser", stream_url])
    else:
        process = subprocess.Popen(["chromium-browser", "--kiosk", stream_url])

    stream_process = process
    

def get_current_streams():
    # read csv and return list of streams in order
    # expects csvs formatted as name,url
    streams = []
    with open(STREAM_FILE) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        line_count=0
        for row in csv_reader:
            streams.append(row)

    # print update    
    print("Current streams:")
    for stream in streams:
        print(stream)

    return streams 

def accept_connection():

    # init socket
    s = socket.socket()
    server_addr = ('pifour.local', 12019)
    s.bind(server_addr)
    s.listen(1)
    print("started server on", server_addr)
    
    try:
        # loop for getting connections
        while True:
            connection, client_addr = s.accept()
            try:
                print("connection from", client_addr)
                # loop for a single connection/interaction
                while True:
                    data = connection.recv(1024)
                    if data:
                        reply = execute_command(data.decode())
                        connection.sendall(reply.encode()) 
                    else:
                        break
            finally:
                connection.close()
    except Exception as e:
        print(e)
        s.close()
    
def execute_command(command):
    """Commands should come in form 'command argument'"""

    command = command.strip('\n')
    print("Received command", command)
    
    if command == "list":
        # send list of streams available and IDs for selection

        streams = get_current_streams()
        reply = "\n".join(["{}) {}".format(i, streams[i][0]) for i in range(len(streams))])

    elif "change" in command:
        try:
            parts = command.split(" ")
            stream_id = int(parts[1])
            change_stream(stream_id)
            reply = "OK"

        except Exception as e:
            print(e)
            reply = "Error: bad command"

    elif command == "help":
        reply = "Commands\n"
        reply += "list: lists all streams available"
        reply += "change <stream_ID>: directs server to change active stream to specified"

    else:
        print("Received unknown command")
        reply = "Error: unknown command"        

    print("replying", reply)
    return reply
     
def main():
    # start default stream
    global stream_process
    stream_process = None
    change_stream(0)
    
    accept_connection()

    stream_process.terminate()

if __name__ == "__main__":
    main()
