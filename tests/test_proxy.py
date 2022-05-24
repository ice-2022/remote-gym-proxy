import gym
from remote_gym_proxy.proxy import Proxy


class TestProxy(Proxy):

    def create_env_custom(self):
        return gym.make('CartPole-v0')


if __name__ == "__main__":
    proxy = TestProxy()
    env1_no = 11
    env2_no = 12
    env1 = proxy.create_env(env1_no)
    env2 = proxy.create_env(env2_no)
    assert proxy.env_num() == 2
    env1_load = proxy.find_env(env1_no)
    assert env1_load == env1
    proxy.remove_env(env1_no)
    assert proxy.env_num() == 1
    proxy.create_env(env1_no)
    proxy.remove_all()
    assert proxy.env_num() == 0




