from gym_network import Client
import gym_core
import test_core_address

client = Client(address=test_core_address.address, port=test_core_address.port)
env = core.RemoteEnv(client)

print("env:")
print("action: ", env.action_space)
print("observation_space: ", env.observation_space)

print("reset")
print("observation:", env.reset())

print("step1")
print("result:", env.step(env.action_space.sample()))

print("step2")
print("result:", env.step(env.action_space.sample()))

