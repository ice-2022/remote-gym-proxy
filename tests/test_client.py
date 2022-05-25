import client


cli = client.Client(address="127.0.0.1", port=9527)
env = client.RemoteEnv(client=cli)
print(env.observation_space)
print(env.action_space)


obs = env.reset()
print(obs)

obs, reword, done = env.step(action=env.action_space.sample())
print("obs:", obs)
print("reword:", reword)
print("done:", done)

cli.close()
