import json


def json_to_dict(json_str):
    """
    Method to safely parse json to dict
    :param json_str: string
    :return: dict
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return json_str


def flatten_dict(response):
    """
    Method to flatten nested records in a dict
    :param d: dict
    :return: dict
    """
    flatten_response = {}

    def flatten(data, name=''):
        if type(data) is dict:
            for datum in data:
                flatten(data[datum], name + datum + '_')
        else:
            flatten_response[name[:-1]] = data

    flatten(response)
    return flatten_response


