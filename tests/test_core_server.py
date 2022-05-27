from gym_core import GymServer
import gym
from gym_core import GymProxy
import test_core_address


class TestProxy(GymProxy):
    def create_env_custom(self):
        env = gym.make('CartPole-v0')
        return env


test_proxy = TestProxy()
gym_server = GymServer(address=test_core_address.address, port=test_core_address.port, gym_proxy=test_proxy)
gym_server.start()
