import socket
import sys

strUsage = """Next-Generation Wireless Network HW2-Server:

Usage:
\tserver.py --port port_number
"""

HOST_IP = "0.0.0.0"
PORT = 10000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main(argv):
    if len(argv) == 1:
        print(strUsage)
        return

    if argv[1] != "--port":
        print(f"Unknown argument: {argv[1]}")
        return

    PORT = int(argv[2])

    s.bind(("0.0.0.0", PORT))
    # Max number of connection = 1
    print(f"Listen on port {PORT}")
    s.listen(1)

    while True:
        try:
            conn, _ = s.accept()
            while True:
                received = conn.recv(1024)
                if len(received) == 0:
                    conn.close()
                    break
                print(received.decode())

                conn.send("test response".encode())
        # When user press Ctrl+C
        except KeyboardInterrupt:
            conn.close()

    s.close()
    print("Server closed")


if __name__ == "__main__":
    main(sys.argv)