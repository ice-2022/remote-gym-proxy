from proxy import Proxy
import gym
from server import Server


class TestProxy(Proxy):
    def create_env_custom(self):
        env = gym.make('CartPole-v0')
        return env


test_proxy = TestProxy()
test_server = Server(address="127.0.0.1", port=9527, proxy=test_proxy)
test_server.start()
