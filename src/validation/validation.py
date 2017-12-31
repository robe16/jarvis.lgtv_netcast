from jsonschema import validate
import json
import os


def validate_keyInput(inpt):
    schema = _get_schema('command_keyInput')
    return _validate_schema(inpt, schema)


def validate_executeApp(inpt):
    schema = _get_schema('command_executeApp')
    return _validate_schema(inpt, schema)


def validate_touchMove(inpt):
    schema = _get_schema('command_touchMove')
    return _validate_schema(inpt, schema)


def validate_touchWheel(inpt):
    schema = _get_schema('command_touchWheel')
    return _validate_schema(inpt, schema)


def _validate_schema(inpt, schema):
    try:
        validate(inpt, schema)
        return True
    except:
        return False


def _get_schema(filename):
    #
    filename = '{filename}.schema.json'.format(filename=filename)
    #
    with open(os.path.join(os.path.dirname(__file__), 'schemas', filename), 'r') as data_file:
        return json.load(data_file)
