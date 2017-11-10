import os
import json
from tests.validation.testlist import testlist
from src.validation.validation import validate_command


def run_test():
    for t in testlist:
        #
        j = _get_json(t['fileName'])
        #
        if t['schema']=='command':
            result = validate_command(j)
        #
        str_result = 'PASS' if result==t['expectedResult'] else 'FAIL'
        #
        print('Test #{id}::{str_result}::expected={expect}-v-result={result}'.format(id=str(t['id']),
                                                                                     str_result=str_result,
                                                                                     expect=t['expectedResult'],
                                                                                     result=result))


def _get_json(filename):
    with open(os.path.join(os.path.dirname(__file__), 'test_files', '{filename}.json'.format(filename=filename)), 'r') as data_file:
        return json.load(data_file)
