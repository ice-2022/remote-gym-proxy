import json
import agent_space_encoder
import numpy as np



class Protocol:
    def __init__(self):
        self.raw = None
        self.obj = None
        self.code = None

    def _code(self):
        raise NotImplementedError()

    def set_raw(self, raw):
        self.raw = raw

    def set_obj(self, obj):
        self.obj = obj


    def encode(self):
        raise NotImplementedError()

    def decode(self):
        raise NotImplementedError()


    REQUEST_EXIT = -1
    REQUEST_SPACE = 1
    RESPONSE_SPACE = 101
    REQUEST_RESET = 2
    RESPONSE_RESET = 102
    REQUEST_STEP = 3
    RESPONSE_STEP = 103

    def __init__(self, code, value):
        self.code = code
        self.value = value
        self.value_json = None
        if value:
            # 如果转不了json，就用原串
            self.value_json = json.loads(value)
            if not self.value_json
        print(value)
        print("value_json", self.value_json)

    def to_bytes(self):
        b = {
            "code": self.code,
            "value": self.value
        }
        return json.dumps(b).encode('utf-8')

    def __str__(self):
        return "code:" + str(self.code) + ", value=" + json.dumps(self.value)


class RequestSpace(Protocol):
    def __init__(self):
        super(RequestSpace, self).__init__(code=Protocol.REQUEST_SPACE, value=None)


class ResponseSpace(Protocol):
    PROT_ID = 1
    def __init__(self, action_space, observation_space):
        self.action_space = action_space
        self.observation_space = observation_space
        value_json = {
            "action_space": agent_space_encoder.encode_agent_space_to_json(action_space),
            "observation_space": agent_space_encoder.encode_agent_space_to_json(observation_space)
        }
        value = json.dumps(value_json).encode("utf-8")
        super(ResponseSpace, self).__init__(code=Protocol.RESPONSE_SPACE, value=value)

    def encode(self):
        value_json = {
            "action_space": agent_space_encoder.encode_agent_space_to_json(self.action_space),
            "observation_space": agent_space_encoder.encode_agent_space_to_json(self.observation_space)
        }
        data = {
            "code": self.code,
            "raw": value_json,
        }
        return json.dumps(data).encode("utf-8")

    def decode(self):
        value_json = json.loads(str)
        input_str = self.raw.decode('utf-8')


class RequestReset(Protocol):
    def __init__(self):
        super(RequestReset, self).__init__(code=Protocol.REQUEST_RESET, value=None)


class ResponseReset(Protocol):
    def __init__(self, observation):
        self.observation = observation
        value_json = {
            "observation": observation.tolist(),
        }
        value = json.dumps(value_json).encode("utf-8")
        super(ResponseReset, self).__init__(code=Protocol.RESPONSE_RESET, value=value)


class RequestStep(Protocol):
    def __init__(self, action):
        self.action = action
        super(RequestStep, self).__init__(code=Protocol.REQUEST_STEP, value={"action": action})


class ResponseStep(Protocol):
    def __init__(self, observation, reward, done):
        self.observation = observation
        self.reward = reward
        self.done = done
        value_json = {
            "observation": observation.tolist(),
            "reward": reward,
            "done": done,
        }
        value = json.dumps(value_json).encode("utf-8")
        super(ResponseStep, self).__init__(code=Protocol.RESPONSE_STEP, value=value)



def to_protocol(input_bytes):
    input_str = input_bytes.decode('utf-8')
    print("input_str: ", input_str)
    input_json = json.loads(input_str)
    code = input_json["code"]
    if code == Protocol.REQUEST_SPACE:
        return RequestSpace()
    elif code == Protocol.RESPONSE_SPACE:
        return ResponseSpace(
            action_space=agent_space_encoder.decode_agent_space_from_json(input_json["value"]["action_space"]),
            observation_space=agent_space_encoder.decode_agent_space_from_json(input_json["value"]["observation_space"])
        )
    elif code == Protocol.REQUEST_RESET:
        return RequestReset()
    elif code == Protocol.RESPONSE_RESET:
        return ResponseReset(np.array(input_json["value"]["observation"]))
    elif code == Protocol.REQUEST_STEP:
        return RequestStep(action=np.array(input_json["value"]["action"]))
    elif code == Protocol.RESPONSE_STEP:
        return ResponseStep(
            observation=np.array(input_json["value"]["observation"]),
            reward=input_json["value"]["reward"],
            done=input_json["value"]["done"],
        )


test_json_b = b'{"code":1}'
obj = to_protocol(test_json_b)
print(obj)
