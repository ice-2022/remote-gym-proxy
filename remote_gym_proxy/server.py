import socket
import threading
import network_protocol
from network_protocol import Protocol
from proxy import Proxy


class Server:
    def __init__(self, address="127.0.0.1", port=9527, proxy=None):
        self.address = address
        self.port = port
        self.running = False
        self.proxy = proxy
        self.workplaces = {}

    def after_connected(self):
        pass

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.address, self.port))
        s.listen(5)
        print("proxy === ", self.proxy)
        print('Waiting for connection...')

        # 等待连接
        while True:
            # 接受一个新连接:
            processing_socket, processing_address = s.accept()
            self.after_connected()
            # 创建新线程来处理TCP连接:
            t = threading.Thread(target=self.process_link, args=(processing_socket, processing_address))
            t.start()

    def process_link(self, processing_socket, processing_address):
        print('Accept new connection from %s:%s...' % processing_address)
        while True:
            client_id = processing_socket.fileno()
            data = processing_socket.recv(1024)
            if not data:
                # 这是断开了
                self.proxy.remove_env(client_id)
                print("连接断开了, client: ", client_id)
                continue

            protocol = network_protocol.to_protocol(data)
            response = None

            if protocol.code == Protocol.REQUEST_SPACE:
                print("收到 Protocol.REQ_SPACE 指令")
                env = self.proxy.get_or_create_env(client_id)
                action_space = env.action_space
                observation_space = env.observation_space
                rep_space = network_protocol.ResponseSpace(
                    action_space=action_space,
                    observation_space=observation_space)
                response = rep_space.to_bytes()

            elif protocol.code == Protocol.REQUEST_RESET:
                print("收到 Protocol.REQUEST_RESET 指令")
                env = self.proxy.get_or_create_env(client_id)
                observation = env.reset()
                reset = network_protocol.ResponseReset(observation=observation)
                response = reset.to_bytes()

            elif protocol.code == Protocol.REQUEST_STEP:
                print("收到 Protocol.REQUEST_STEP 指令")
                env = self.proxy.get_or_create_env(client_id)
                observation, reward, done = env.step(protocol.action)
                step = network_protocol.ResponseStep(
                    observation=observation,
                    reward=reward,
                    done=done
                )
                response = step.to_bytes()

            processing_socket.send(response)

        # processing_socket.close()
        print('Connection from %s:%s closed.' % processing_address)



s = Server(address="127.0.0.1", port=9527, )