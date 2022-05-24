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
        self.socket.send(request_space.to_bytes())
        space_data = self.socket.recv(1024)
        response_space = network_protocol.to_protocol(space_data)
        self.action_space = response_space.action_space
        self.observation_space = response_space.observation_space


    def reset(self):
        cmd = {"type": "reset"}
        self.socket.send(json.dumps(cmd).encode("utf-8"))
        info = self.socket.recv(1024).decode('utf-8')
        obs_json = json.loads(info)
        return np.array(obs_json)

    def close(self):
        self.socket.close()

    def step(self, action):
        cmd = {"type": "step", "action": action.tolist()}
        self.socket.send(json.dumps(cmd).encode("utf-8"))
        back = self.socket.recv(1024).decode('utf-8')
        result = json.loads(back)
        return np.array(result["observation"]), result["reward"], result["done"], result["info"]