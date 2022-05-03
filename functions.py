import json


def dump(value):
    print((json.dumps(value, indent=4, sort_keys=True)))
