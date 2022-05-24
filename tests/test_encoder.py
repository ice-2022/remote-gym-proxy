from gym.spaces.discrete import Discrete
from gym.spaces.box import Box
import numpy as np
from remote_gym_proxy import agent_space_encoder

if __name__ == "__main__":
    # 测试 Discrete 类
    test_discrete1 = Discrete(10)
    test_discrete_json = encoder.encode_discrete(test_discrete1)
    print(test_discrete_json)
    test_discrete2 = encoder.decode_discrete(test_discrete_json)
    print("test_discrete1:", test_discrete2)
    print("test_discrete2:", test_discrete2)
    assert test_discrete1 == test_discrete2

    print()

    # 测试 box 类
    test_box1 = Box(-np.inf, np.inf, shape=(2,), dtype=np.float32)
    test_box_json = encoder.encode_box(test_box1)
    print(test_box_json)
    test_box2 = encoder.decode_box(test_box_json)
    print("test_box1:", test_box1)
    print("test_box2:", test_box2)
    assert test_box1 == test_box2


