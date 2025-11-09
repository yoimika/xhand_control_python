import socket
import os

class Socket:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.server_socket = None
        self.client_socket = None
        self.client_address = None

    def listen(self)->None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print("Waiting for connection...")
        self.client_socket, self.client_address = self.server_socket.accept()
        print("Connected to: ", self.client_address)

    def send(self, sent_data: str)->None:
        byte_data = sent_data.encode('utf-8')
        self.client_socket.send(byte_data)
    
    def receive(self)->str:
        received_data = self.client_socket.recv(2048)
        if not received_data:
            return None
        received_data = received_data.decode('utf-8')
        return received_data

    def communicate_with_client(self):
        self.send()
    
    def reset_connection(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            self.client_address = None
        print("Client disconnected. Resetting connection....")
        self.listen()
    
    def quit(self)->None:
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        print("Socket Manager Quit")
    
    def init(self):
        fp = './record.txt'
        for i in range(100):
            self.send("alksdflasjdfljaslk")
            data = self.receive()

            with open(fp, encoding='utf-8', mode='r') as f:
                content = f.read()
            content += data
            length = int(content[:6])
            print(f"Length: {length}")
            data = content[7:]

            if len(data) < length:
                rec_data = 'asldfjlkasjlkgjslkajdfljasldfjlasdkjf'
                save_data = content
            elif len(data) == length:
                rec_data = data
                save_data = content
            else:
                length2 = int(data[length:length+6])
                data2 = data[length+7:]
                if len(data2) < length2:
                    rec_data = data[:length]
                    save_data = content
                else:
                    rec_data = data2[:length2]
                    save_data = data[length:]

            with open(fp, encoding='utf-8', mode='w') as f:
                f.write(save_data)

            # print("Data: " + rec_data)
    def rec(self):
        fp = './record.txt'
        self.send("alksdflasjdfljaslk")
        data = self.receive()

        with open(fp, encoding='utf-8', mode='r') as f:
            content = f.read()
        content += data
        length = int(content[:6])
        print(f"Length: {length}")
        data = content[7:]

        if len(data) < length:
            rec_data = 'asldfjlkasjlkgjslkajdfljasldfjlasdkjf'
            save_data = content
        elif len(data) == length:
            rec_data = data
            save_data = content
        else:
            length2 = int(data[length:length+6])
            data2 = data[length+7:]
            if len(data2) < length2:
                rec_data = data[:length]
                save_data = content
            else:
                rec_data = data2[:length2]
                save_data = data[length:]

        with open(fp, encoding='utf-8', mode='w') as f:
            f.write(save_data)
        return rec_data

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 54321
    socket_manager = Socket(host=host, port=port)
    socket_manager.listen()

    fp = './record.txt'
    with open(fp, encoding='utf-8', mode='w') as f:
        pass

    while True:
        socket_manager.send("alksdflasjdfljaslk")
        data = socket_manager.receive()

        with open(fp, encoding='utf-8', mode='r') as f:
            content = f.read()
        content += data
        length = int(content[:6])
        print(f"Length: {length}")
        data = content[7:]

        if len(data) < length:
            rec_data = 'asldfjlkasjlkgjslkajdfljasldfjlasdkjf'
            save_data = content
        elif len(data) == length:
            rec_data = data
            save_data = content
        else:
            length2 = int(data[length:length+6])
            data2 = data[length+7:]
            if len(data2) < length2:
                rec_data = data[:length]
                save_data = content
            else:
                rec_data = data2[:length2]
                save_data = data[length:]

        with open(fp, encoding='utf-8', mode='w') as f:
            f.write(save_data)

        print("Data: " + rec_data)
