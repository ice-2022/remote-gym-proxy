import time
import flappy_bird_gym
from remote_gym_proxy.core import AgentClient
import numpy as np

env = flappy_bird_gym.make("FlappyBird-v0")
agent = AgentClient(address="127.0.0.1", port=9999)

obs = env.reset()
while True:
    # Next action:
    # (feed the observation to your agent here)
    response = agent.request_action(obs)
    action = np.int32(response)

    # Processing:
    obs, reward, done, info = env.step(action)

    # Rendering the game:
    # (remove this two lines during training)
    env.render()
    time.sleep(1 / 30)  # FPS

    # Checking if the player is still alive
    if done:
        break

env.close()