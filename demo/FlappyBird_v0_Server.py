import flappy_bird_gym
from remote_gym_proxy.core import GymServer
from remote_gym_proxy.core import GymProxy


class CartPoleV0Proxy(GymProxy):
    def create_env_custom(self):
        return flappy_bird_gym.make("FlappyBird-v0")


cart_proxy = CartPoleV0Proxy()
gym_server = GymServer(address="127.0.0.1", port=9527, gym_proxy=cart_proxy)
gym_server.start()
