import socket
import sys

strUsage = """Next-Generation Wireless Network HW2-Client:

Usage:
\tclient.py --host host_ip --port port_number
"""

HOST_IP = "127.0.0.1"
PORT = 10000

def main(argv):
    if len(argv) == 1:
        print(strUsage)
        return

    for index in range(len(argv)):
        if argv[index] == "--host":
            HOST_IP = argv[index + 1]
        elif argv[index] == "--port":
            PORT = int(argv[index + 1])

    while True:
        print("Mode1: single-line process")
        print("Mode2: batch process")
        mode = input("Choose your mode(1, 2 or q(quit)):")

        if mode == "q":
            print("Exit")
            return

        if mode == "1":
            mode1()

def mode1():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST_IP, PORT))
        
        while True:
            message = input("> ")

            # Default encoding: UTF-8
            s.send(message.encode())
            received = s.recv(1024)

            # Default decoding: UTF-8
            print(received.decode())

        s.close()



if __name__ == "__main__":
    main(sys.argv)