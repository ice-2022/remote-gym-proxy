from gym_core import GymServer
import gym
from gym_core import GymProxy


class CartPoleV0Proxy(GymProxy):
    def create_env_custom(self):
        env = gym.make('CartPole-v0')
        return env


cart_proxy = CartPoleV0Proxy()
gym_server = GymServer(address="127.0.0.1", port=9527, gym_proxy=cart_proxy)
gym_server.start()
