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
import gym
from remote_gym_proxy.core import GymServer
from remote_gym_proxy.core import GymProxy


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
from remote_gym_proxy.core import RemoteEnv
import numpy as np

env = RemoteEnv(address="127.0.0.1", port=9527)
print("env:")
print("action: ", env.action_space)
print("observation_space: ", env.observation_space)
print("-" * 20)
print("reset")
print("observation:", env.reset())
print("-" * 20)
print("step1")
print("result1:", env.step(np.int32(env.action_space.sample())))
print("-" * 20)
print("step2")
print("result2:", env.step(np.int32(env.action_space.sample())))
print("-" * 20)
env.close()
```

## Client-Demo with training
