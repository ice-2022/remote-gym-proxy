import gym


class Proxy:
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
        print(self.agents.keys())
        del self.agents[env_id]

    def remove_all(self):
        self.agents.clear()

    def env_num(self):
        return len(self.agents.keys())

