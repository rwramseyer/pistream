#!/usr/env/bin python3
# pistream_server.py
# This program runs on the pi and displays available
# streams and allows stream selection

import socket
import csv

STREAM_FILE = "stream_options.csv"

def change_stream(stream_id):
    stream = get_current_streams()[stream_id]
    print(stream)

def get_current_streams():
    # read csv and return list of streams in order
    # expects csvs formatted as name,url
    streams = []
    with open(STREAM_FILE) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        line_count=0
        for row in csv_reader:
           print(row)

    return streams 

def accept_connections():

    # init socket
    s = socket.socket()
    server_addr = ('localhost', 12019)
    print("starting server on", server_addr)
    s.bind(server_addr)
    s.listen(1)

    while True:
        connection, client_addr = s.accept()
        try:
            print("connection from", client_addr)

            message = "" 
            while True:
                data = connection.recv(1024)
                if data:
                    message += data
                else:
                    break

            if message:
                reply = execute_command(message)
                connection.sendall(reply) 

        finally:
            connection.close()
    
def execute_command(message):
    """Commands should come in form 'command argument'"""

    command_list = ["help", "list", "add", "change", "delete"]
    
    msg_parts = message.split(" ")
    command = msg_parts[0]
    print("recieved command", command)
    
    if command == "list":
        # send list of streams available and IDs for selection
        pass
    elif command == "change":
        pass
    elif command == "add":
        # add given name and
        pass
    elif command == "delete":
        pass
    elif command == "help":
        reply = "Commands\n"
        reply += "list: lists all streams available"
        reply += "change <stream_ID>: directs server to change active stream to specified"
        reply += "add <stream_name> <URL>: adds new stream to permanent list"
        reply += "delete <stream_ID>: deletes stream from permanent list"
    else:
        print("Received unknown command")
        reply = "Error: unkown command"        

    return reply
     
def main():
    # start default stream
    change_stream(1)

    # wait for connections
    accept_connections()


if __name__ == "__main__":
    main()
