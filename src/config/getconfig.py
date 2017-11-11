import requests
from socket import gethostbyname, gethostname
from resources.global_resources.variables import uri_configService
from config.discovery import discover_server


def get_config(service_id, self_port):
    #
    result_get = _get(service_id)
    #
    if bool(result_get):
        result_set = _set(service_id, self_port)
        if bool(result_set):
            return result_get
    #
    return False


def _get(service_id):
    #
    try:
        #
        server_url = _url(service_id)
        #
        r = requests.get(server_url)
        #
        if r.status_code == requests.codes.ok:
            return r.json
        else:
            return False
        #
    except:
        return False


def _set(service_id, self_port):
    #
    try:
        #
        data = {"id": service_id,
                "ipaddress": my_ip(),
                "port": self_port}
        #
        server_url = _url(id)
        #
        r = requests.post(server_url, body=data)
        #
        if r.status_code == requests.codes.ok:
            return True
        else:
            return False
    except:
        return False


def _url(service_id):
    #
    try:
        server_address = discover_server()
    except:
        raise Exception
    #
    return 'http://{server_address}{uri}'.format(server_address=server_address,
                                                 uri=uri_configService.format(service_id=service_id))

def my_ip():
    return gethostbyname(gethostname())
