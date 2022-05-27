# remote-gym-proxy

## Install
```shell
git clone git@github.com:ice-2022/remote-gym-proxy.git
cd remote-gym-proxy
python setup.py install
```

## Server-Demo
give gym.Env through GymProxy.create_env_custom, and give GymServer, the server is finish!
```python
from core import GymServer
import gym
from core import GymProxy

class CartPoleV0Proxy(GymProxy):
    def create_env_custom(self):
        env = gym.make('CartPole-v0')
        return env
cart_proxy = CartPoleV0Proxy()
gym_server = GymServer(address="127.0.0.1", port=9527, gym_proxy=cart_proxy)
gym_server.start()
```

## Client-Demo

```python
from gym_network import Client
import gym_core

client = Client(address="127.0.0.1", port=9527)
env = core.RemoteEnv(client)

print("env.action: ", env.action_space)
print("env.observation_space: ", env.observation_space)
print("exec reset")
print("observation:", env.reset())
print("exec reset1")
print("result1:", env.step(env.action_space.sample()))
print("exec reset2")
print("result2:", env.step(env.action_space.sample()))

client.close()
```

## Client-Demo with training
