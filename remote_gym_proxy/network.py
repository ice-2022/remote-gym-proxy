"""
A simple tcp server with a long base protocol
"""
import socket
import threading
import struct
import json
import traceback


def send_str(client_socket, str_data):
    bytes_data = str_data.encode("utf-8")
    length_data = len(bytes_data)
    length_protocol = 4 + length_data
    bytes_send = struct.pack('hh{n}s'.format(n=length_data), length_protocol, length_data, bytes_data)
    client_socket.send(bytes_send)


def send_json(client_socket, json_data):
    str_data = json.dumps(json_data)
    send_str(client_socket, str_data)


class Server:
    def __init__(self, address="127.0.0.1", port=9527):
        self.address = address
        self.port = port
        self.running = False

    def _handle_request(self, bytes_data, processing_socket):
        raise NotImplementedError()

    def _handle_connection_close(self, processing_socket):
        raise NotImplementedError()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.address, self.port))
        server_socket.listen(5)
        print("Server started, ip:", self.address, ",port:", self.port)
        print('Waiting for connection...')

        # 等待连接
        while True:
            # 接受一个新连接:
            processing_socket, processing_address = server_socket.accept()
            processing_socket.settimeout(5)
            # 创建新线程来处理TCP连接:
            t = threading.Thread(target=self.process_link, args=(processing_socket, processing_address))
            t.start()

    def process_link(self, processing_socket, processing_address):
        print('Accept new connection from %s:%s...' % processing_address)
        buffer = b''
        while True:
            data = None
            try:
                data = processing_socket.recv(1024)
                if not data:
                    print("client Connection close, fire event")
                    self._handle_connection_close(processing_socket=processing_socket)
                    break
            except ConnectionResetError:
                print("client Connection close, fire event")
                self._handle_connection_close(processing_socket=processing_socket)
                break

            # 解决粘包和分包相关的问题 协议标准是 hhs -(长度)> 11n
            buffer += data
            while True:
                length_buffer = len(buffer)
                if length_buffer < 5:
                    break

                length_protocol, length_str = struct.unpack('hh', buffer[:4])
                if length_protocol > length_buffer:
                    # 数据没有发完，回去外循环等待
                    break

                (bytes_data,) = struct.unpack('{n}s'.format(n=length_str), buffer[4:length_buffer + 4])
                buffer = buffer[length_buffer + 4:]
                try:
                    self._handle_request(bytes_data, processing_socket)
                except Exception:
                    print("客户端的请求，处理异常，IP:", processing_address)
                    processing_socket.close()
                    traceback.print_exc()

        processing_socket.close()
        print('Connection from %s:%s closed.' % processing_address)


class Client:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 建立连接:
        self.socket.connect((self.address, self.port))

    def send(self, str_data):
        send_str(self.socket, str_data)

    def request(self, str_data):
        send_str(self.socket, str_data)
        buffer = b''
        while True:
            data = self.socket.recv(1024)
            if not data:
                print("服务器数据返回异常")
                self.socket.close()
                return None

            # Deal sticky, packet, unpacking in communications
            # the struct format is "hhs", so the length is 2,2,n
            buffer += data
            while True:
                length_buffer = len(buffer)
                if length_buffer < 5:
                    break

                length_protocol, length_str = struct.unpack('hh', buffer[:4])
                if length_protocol > length_buffer:
                    break

                (str_data,) = struct.unpack('{n}s'.format(n=length_str), buffer[4:length_buffer + 4])
                return str_data

    def close(self):
        self.socket.close()

