import json
import agent_space_encoder


class Space:
    def __init__(self):
        print("space")


class Protocol:
    REQUEST_EXIT = -1
    REQUEST_SPACE = 1
    RESPONSE_SPACE = 101

    def __init__(self, code, value):
        self.code = code
        self.value_json = None
        if value:
            self.value_json = json.loads(value)

    def to_bytes(self):
        b = {
            "code": self.code,
            "value": self.value_json
        }
        return json.dumps(b).encode('utf-8')

    def __str__(self):
        return "code:" + str(self.code) + ", value=" + json.dumps(self.value_json)


class RequestSpace(Protocol):
    def __init__(self):
        super(RequestSpace, self).__init__(code=Protocol.REQUEST_SPACE, value=None)


class ResponseSpace(Protocol):
    def __init__(self, action_space, observation_space):
        self.action_space = action_space
        self.observation_space = observation_space
        value_json = {
            "action_space": agent_space_encoder.encode_agent_space_to_json(action_space),
            "observation_space": agent_space_encoder.encode_agent_space_to_json(observation_space)
        }
        super(ResponseSpace, self).__init__(code=Protocol.RESPONSE_SPACE, value=value_json)


def to_protocol(input_bytes):
    input_str = input_bytes.decode('utf-8')
    print(input_str)
    input_json = json.loads(input_str)
    code = input_json["code"]
    if code == Protocol.REQUEST_SPACE:
        return RequestSpace()
    elif code == Protocol.RESPONSE_SPACE:
        return ResponseSpace(
            action_space=agent_space_encoder.decode_agent_space_from_json(input_json["value"]["action_space"]),
            observation_space=agent_space_encoder.decode_agent_space_from_json(input_json["value"]["observation_space"])
        )


test_json_b = b'{"code":1}'
obj = to_protocol(test_json_b)
print(obj)
