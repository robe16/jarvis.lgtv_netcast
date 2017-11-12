import json
import os
import ast

file_name = 'config.json'


def write_config(new_data):
    try:
        #
        try:
            new_data = ast.literal_eval(new_data)
        except:
            new_data = new_data
        #
        with open(os.path.join(os.path.dirname(__file__), file_name), 'w+') as output_file:
            output_file.write(json.dumps(new_data, indent=4, separators=(',', ': ')))
            output_file.close()
        #
        return True
    except Exception as e:
        return False


def get_config_json():
    #
    with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as data_file:
        return json.load(data_file)


def get_cfg_serviceid():
    return get_config_json()['service_id']


def get_cfg_name():
    return get_config_json()['name']


def get_cfg_groups():
    return get_config_json()['groups']


def get_cfg_details():
    return get_config_json()['details']


def get_cfg_details_ip():
    return get_cfg_details()['ipaddress']


def get_cfg_details_pairingkey():
    return get_cfg_details()['pairingkey']
