"""
A Gym Env TCP Proxy, for rl.
Something the training env is different from the actor env
"""

import numpy as np

from remote_gym_proxy.network import send_json
from remote_gym_proxy.network import Server
from remote_gym_proxy.network import Client
from remote_gym_proxy import gym_encoder
import json
import gym


class GymServer(Server):
    def __init__(self, address, port, gym_proxy):
        super(GymServer, self).__init__(address=address, port=port)
        self.gym_proxy = gym_proxy

    def _handle_connection_close(self, processing_socket):
        client_id = processing_socket.fileno()
        env = self.gym_proxy.get_or_create_env(client_id)
        env.close()
        self.gym_proxy.remove_env(client_id)
        print("删除env成功，client_id:", client_id)

    def _handle_request(self, bytes_data, processing_socket):
        client_id = processing_socket.fileno()
        str_data = bytes_data.decode('utf-8')
        json_data = json.loads(str_data)
        code = json_data["code"]
        env = self.gym_proxy.get_or_create_env(client_id)
        if code == 1:
            # process space
            json_response = {
                "code": 1001,
                "value": {
                    "action_space": gym_encoder.encode_agent_space_to_json(env.action_space),
                    "observation_space": gym_encoder.encode_agent_space_to_json(env.observation_space),
                }
            }
            send_json(processing_socket, json_response)

        elif code == 2:
            # process reset
            observation = env.reset()
            json_response = {
                "code": 1002,
                "value": observation.tolist()
            }
            send_json(processing_socket, json_response)

        elif code == 3:
            # process step
            action = json_data["value"]
            observation, reward, done, info = env.step(action)
            json_response = {
                "code": 1003,
                "value": {
                    "observation": observation.tolist(),
                    "reward": reward,
                    "done": done,
                }
            }
            send_json(processing_socket, json_response)


class RemoteEnv(gym.Env):
    def __init__(self, address, port):
        self.client = Client(address=address, port=port)
        self.client.connect()
        # init space info
        action_space, observation_space = self._get_space()
        self.action_space = action_space
        self.observation_space = observation_space

    def _get_space(self):
        bytes_data = self.client.request('{"code": 1}')
        json_data = json.loads(bytes_data.decode('utf-8'))
        value = json_data["value"]
        action_space = gym_encoder.decode_agent_space_from_json(value["action_space"])
        observation_space = gym_encoder.decode_agent_space_from_json(value["observation_space"])
        return action_space, observation_space

    def step(self, action):
        json_request = {
            "code": 3,
            "value": action.tolist(),
        }
        bytes_data = self.client.request(json.dumps(json_request))
        json_data = json.loads(bytes_data.decode("utf-8"))
        value = json_data["value"]
        return np.array(value["observation"]), value["reward"], value["done"], {}

    def reset(self):
        bytes_data = self.client.request('{"code": 2}')
        json_data = json.loads(bytes_data.decode('utf-8'))
        return np.array(json_data["value"])

    def render(self, mode='human'):
        pass

    def close(self):
        self.client.close()


class GymProxy:
    def __init__(self):
        self.agents = {}

    def create_env_custom(self):
        raise NotImplementedError

    def get_or_create_env(self, env_id):
        if env_id in self.agents:
            return self.agents[env_id]
        return self.create_env(env_id)

    def create_env(self, env_id):
        env = self.create_env_custom()
        if not isinstance(env, gym.Env):
            raise ValueError()
        self.agents[env_id] = env
        return env

    def find_env(self, env_id):
        return self.agents[env_id]

    def remove_env(self, env_id):
        del self.agents[env_id]

    def remove_all(self):
        self.agents.clear()

    def env_num(self):
        return len(self.agents.keys())


class AgentServer(Server):
    def __init__(self, address, port, trainer):
        super(AgentServer, self).__init__(address=address, port=port)
        self.trainer = trainer

    def _handle_request(self, bytes_data, processing_socket):
        json_data = json.loads(bytes_data.decode("utf-8"))
        observation = np.array(json_data["observation"])
        action = self.trainer.compute_single_action(observation)
        response = {
            "action": action.tolist()
        }
        send_json(processing_socket, response)

    def _handle_connection_close(self, processing_socket):
        print("关闭服务器")


class AgentClient:
    def __init__(self, address, port):
        self.client = Client(address=address, port=port)
        self.client.connect()

    def request_action(self, observation):
        json_request = {
            "observation": observation.tolist()
        }
        data = self.client.request(json.dumps(json_request))
        json_data = json.loads(data)
        return json_data["action"]