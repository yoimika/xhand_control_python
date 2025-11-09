import socket
# from typing import override
import multiprocessing
import threading

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
    
class DoubleBufferClient(Socket):
    def __init__(self, host, port):
        super().__init__(host, port)

        self.buffer = None
        self.is_running = False
        self.lock = threading.Lock()
        self.thread = None
        # self.manager = multiprocessing.Manager()
        # self.data_manager = self.manager.Namespace()
        # self.data_manager.buffer = None

        self._length_offset = 0
        self._length_size = 6
        self._data_offset = 7

        self._damn_message = '嘉然今天吃什么'
    
    # @override
    def listen(self)->None:
        super().listen()
        
        with self.lock:
            self.is_running = True
        
        self.thread = threading.Thread(target=self._update_buffer, daemon=True)
        self.thread.start()
        # self.process = multiprocessing.Process(target=self._update_buffer)
        # self.process.daemon = True
        # self.process.start()
    
    def _is_data_length_valid(self, data):
        return len(data) >= self._length_offset + self._length_size

    def _is_data_valid(self, data):
        if self._is_data_length_valid(data):
            length = self._get_data_length(data)
            return len(data) >= self._data_offset + length 
        else:
            return False

    def _get_data_length(self, data):
        assert self._is_data_length_valid(data)
        return int(data[self._length_offset:self._length_offset+self._length_size])
    
    def _get_data_info(self, data, cut_data=False):
        assert self._is_data_valid(data)
        length = self._get_data_length(data)
        ret_data = data[self._data_offset:self._data_offset+length]
        if cut_data:
            _data = data[self._data_offset+length:]
            return length, ret_data, _data
        return length, ret_data, None
        
    def _update_buffer(self):
        buffer2 = ""
        while True:
            # self.send(self._damn_message)
            rec_data = self.receive()

            buffer2 += rec_data
            if self._is_data_valid(buffer2) is not True:
                continue
            else:
                next_data = buffer2
                while self._is_data_valid(next_data):
                    _, data, next_data = self._get_data_info(next_data, cut_data=True)

                # self.data_manager.buffer = data
                with self.lock:
                    self.buffer = data
                buffer2 = next_data
    

    def get_data(self):
        # return self.data_manager.buffer
        while self.buffer is None:
            continue
        with self.lock:
            return self.buffer
    
    def stop(self):
        with self.lock:
            self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
        
    # @override
    def quit(self):
        self.stop()
        super().quit()
        
if __name__ == '__main__':
    client = DoubleBufferClient('0.0.0.0', 54321)
    client.listen()

    try:
        while True:
            data = client.get_data()
            print(data, len(data))
    except Exception as e:
        print(e)
        client.quit()