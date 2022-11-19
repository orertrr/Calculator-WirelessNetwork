import socket
import sys

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

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host_IP, port))
    except:
        print(f"Can't connect to the server.")
        return

    while True:
        print("Mode1: single-line process")
        print("Mode2: batch process")
        mode = input("Choose your mode[1, 2 or q(quit)]:")

        if mode == "q":
            print("Exit")
            return

        if mode == "1":
            mode1(s)

        if mode == "2":
            mode2(s)

    

def mode1(s):
    while True:
        message = input("> ")

        if message == "q":
            print("Quit mode1")
            break

        # Default encoding: UTF-8
        s.send(message.encode())
        received = s.recv(1024)

        # Default decoding: UTF-8
        print(received.decode())

    s.close()

def mode2(s):
    return

if __name__ == "__main__":
    main(sys.argv)