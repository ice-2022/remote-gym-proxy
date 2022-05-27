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

