from threading import Thread
import calculator
import socket
import os

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
                print("Waiting for connection...")
                client, _ = self.server.accept()

                mode = client.recv(1024).decode()
                if mode == "single-line mode":
                    self.single_line_mode(client)
                elif mode == "batch mode":
                    self.batch_mode(client)

        except:
            pass

    def single_line_mode(self, client):
        while True:
            receivedBytes = client.recv(1024)
            if len(receivedBytes) == 0:
                client.close()
                break

            receivedMessage = receivedBytes.decode()
            print(f"Received: {receivedMessage}")
            result = calculator.compute(receivedMessage)
            print(f"Send: {result}")
            client.send(result.encode())

        print("Quit")
        print()

    def batch_mode(self, client):
        formulas = []
        while True:
            receivedBytes = client.recv(1024)
            if len(receivedBytes) == 0:
                client.close()
                break

            receivedMessage = receivedBytes.decode()
            print(f"Received: {receivedMessage}")
            formulas.append(receivedMessage)

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Ans.txt")
        with open(path, "w") as file:
            for formula in formulas:
                result = calculator.compute(formula)
                print(f"Ans: {result}")
                file.write(f"{result}\n")

        print("Quit")
        print()