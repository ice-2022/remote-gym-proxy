import gym
import socket
import network_protocol


class RemoteEnv(gym.Env):

    def __init__(self, client):
        self.client = client
        self.client.connect()
        self.action_space = client.action_space
        self.observation_space = client.observation_space

    def step(self, action):
        self.client.step(action)

    def reset(self):
        self.client.reset()

    def render(self, mode='human'):
        pass


class Client:

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.socket = None
        self.action_space = None
        self.observation_space = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 建立连接:
        self.socket.connect((self.address, self.port))

        # 请求 环境的space 相关信息
        request_space = network_protocol.RequestSpace()
        print("11111")
        self.socket.send(request_space.to_bytes())
        space_data = self.socket.recv(1024)
        response_space = network_protocol.to_protocol(space_data)
        self.action_space = response_space.action_space
        self.observation_space = response_space.observation_space

    def reset(self):
        request_reset = network_protocol.RequestReset()
        self.socket.send(request_reset.to_bytes())
        reset_data = self.socket.recv(1024)
        response_reset = network_protocol.to_protocol(reset_data)
        return response_reset.observation

    def close(self):
        self.socket.close()

    def step(self, action):
        request_step = network_protocol.RequestStep(action=action)
        self.socket.send(request_step.to_bytes())
        step_data = self.socket.recv(1024)
        response_step = network_protocol.to_protocol(step_data)
        return response_step.observation, response_step.reward, response_step.done, {}
