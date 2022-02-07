import json


def myconverter(o):
    if isinstance(o, object):
        return o.name.__str__()


def convert_to_json(students_list):
    return json.dumps(students_list, default=myconverter, indent=4)
