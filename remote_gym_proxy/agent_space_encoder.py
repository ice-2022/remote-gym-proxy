import numpy as np
from gym.spaces.discrete import Discrete
from gym.spaces.box import Box


def decode_discrete(data_json):
    n = data_json["n"]
    return Discrete(n)


def encode_discrete(discrete):
    n = discrete.n
    return {
        "n": n
    }


def decode_box(data_json):
    low = np.array(data_json["low"])
    high = np.array(data_json["high"])
    # 数据类型
    dtype = np.dtype(data_json["dtype"])
    return Box(low, high, None, dtype)


def encode_box(box):
    # 数据以np的array方式保存，序列化的时候，要tolist，转成普通的数据格式
    return {
        "low": box.low.tolist(),
        "high": box.high.tolist(),
        "dtype": box.dtype.name
    }


def encode_agent_space_to_json(box_or_discrete):
    if isinstance(box_or_discrete, Box):
        return encode_box(box_or_discrete)
    elif isinstance(box_or_discrete, Discrete):
        return encode_discrete(box_or_discrete)
    else:
        raise ValueError()


def decode_agent_space_from_json(box_or_discrete_json):
    if "n" in box_or_discrete_json:
        return decode_discrete(box_or_discrete_json)
    elif "low" in box_or_discrete_json:
        return decode_box(box_or_discrete_json)
    else:
        raise ValueError()
