import gym_core

env = gym_core.RemoteEnv(address="127.0.0.1", port=9527)

print("env:")
print("action: ", env.action_space)
print("observation_space: ", env.observation_space)

print("reset")
print("observation:", env.reset())

print("step1")
print("result1:", env.step(env.action_space.sample()))

print("step2")
print("result2:", env.step(env.action_space.sample()))

env.close()

