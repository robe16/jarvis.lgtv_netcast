from jsonschema import validate
import json
import os


def validate_command(inpt):
    schema = _get_schema('command')
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
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as data_file:
        return json.load(data_file)
