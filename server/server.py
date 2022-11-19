import sys
import time
from socket_thread import SocketThread

strUsage = """Next-Generation Wireless Network HW2-Server:

Usage:
\tserver.py --port port_number
"""

def main(argv):
    if len(argv) == 1:
        print(strUsage)
        return

    if argv[1] != "--port":
        print(f"Unknown argument: {argv[1]}")
        return

    port = int(argv[2])

    thread = SocketThread(port)
    thread.start()

    # Main thread sleep
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            thread.server.close()
            print("Server closed")
            return

if __name__ == "__main__":
    main(sys.argv)