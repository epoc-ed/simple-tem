import json

def unpack_json(message):
    message = message.replace("'", '"')
    j = json.loads(message)
    return j