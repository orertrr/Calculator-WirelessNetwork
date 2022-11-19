from threading import Thread
import socket

class SocketThread(Thread):

    def __init__(self, port: int):
        super().__init__()
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.server.bind(("0.0.0.0", self.port))
        print(f"Server listen on port {self.port}")

        # Set maximum number of connection to 1
        self.server.listen(1)

        try:    
            while True:
                client, _ = self.server.accept()

                while True:
                    receivedBytes = client.recv(1024)
                    if len(receivedBytes) == 0:
                        client.close()
                        break
                    receivedMessage = receivedBytes.decode()
                    print(f"Received massage: {receivedMessage}")
                    client.send(f"Send: {receivedMessage}".encode())
        except:
            pass