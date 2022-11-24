import socket
import time
import sys
import os

strUsage = """Next-Generation Wireless Network HW2-Client:

Usage:
\tclient.py --host host_ip --port port_number
"""

def main(argv):
    host_IP = "127.0.0.1"
    port = 10000

    if len(argv) == 1:
        print(strUsage)
        return

    for index in range(len(argv)):
        if argv[index] == "--host":
            host_IP = argv[index + 1]
        elif argv[index] == "--port":
            port = int(argv[index + 1])

    while True:
        print("Mode1: single-line process")
        print("Mode2: batch process")
        mode = input("Choose your mode[1, 2 or q(quit)]:")

        if mode == "q":
            print("Exit")
            return

        if mode == "1":
            single_line_mode(host_IP, port)
        elif mode == "2":
            batch_mode(host_IP, port)
        else:
            print("Invalid mode")

def single_line_mode(host, port):
    print(f"Connect to server({host}:{port})")
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((host, port))
    except:
        print(f"Can't connect to the server.")
        return

    server.send("single-line mode".encode())
    print("Enter your formula(or 'q' to quit)")
    while True:
        print()
        message = input("> ")

        if message == "q":
            print("Quit mode1")
            break
        
        # Default encoding: UTF-8
        server.send(message.encode())
        print(f"Send: {message}")

        # Default decoding: UTF-8
        received = server.recv(1024).decode()
        print(f"Received: {received}")

    server.close()
    print("Connection closed")
    print()

def batch_mode(host, port):
    print(f"Connect to server({host}:{port})")
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((host, port))
    except:
        print(f"Can't connect to the server.")
        return

    server.send("batch mode".encode())
    time.sleep(0.01)
    
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Testcase.txt")
    with open(path, "r") as file:
        for line in file:
            # Get rid of '\n'
            if line[-1] == "\n":
                line = line[:-1]
            
            if line == "":
                continue

            server.send(line.encode())
            time.sleep(0.01)

    server.close()

if __name__ == "__main__":
    main(sys.argv)