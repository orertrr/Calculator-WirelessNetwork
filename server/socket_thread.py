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

        except Exception as e:
            print(e)
            return

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

    def batch_mode(self, client: socket.socket):
        # Get client's line separator
        client_lineseparator = client.recv(2).decode()

        # Enqueue:        char_queue + chars
        #
        # Dequeue(index): result = char_queue[:index]
        #                 char_queue = char_queue[index (+ offset):]
        #                 return result
        char_queue = ""
        formulas = []
        while True:
            receivedBytes = client.recv(1024)
            if len(receivedBytes) == 0:
                client.close()
                break

            receivedMessage = receivedBytes.decode()
            char_queue = char_queue + receivedMessage # Enqueue

            newline_index = char_queue.find(client_lineseparator)
            while newline_index >= 0:
                # Dequeue(newline_index)
                formulas.append(char_queue[:newline_index])
                char_queue = char_queue[newline_index + len(client_lineseparator):]
                newline_index = char_queue.find(client_lineseparator)
        
        if len(char_queue) > 0:
            formulas.append(char_queue)

        for formula in formulas:
            if formula[-1] == "\n":
                formula = formula[:-1]
            print(f"Received: {formula}")

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Ans.txt")
        with open(path, "w") as file:
            for formula in formulas:
                result = calculator.compute(formula)
                print(f"Ans: {result}")
                file.write(f"{result}\n")

        print("Quit")
        print()