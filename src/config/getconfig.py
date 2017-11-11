import requests
from resources.global_resources.variables import uri_configService


def get_config(service_id, server_ip, server_port, self_ip, self_port):
    #
    result_get = _get(service_id, server_ip, server_port)
    #
    if bool(result_get):
        result_set = _set(service_id, server_ip, server_port, self_ip, self_port)
        if bool(result_set):
            return result_get
    #
    return False


def _get(service_id, server_ip, server_port):
    #
    server_url = _url(service_id, server_ip, server_port)
    #
    r = requests.get(server_url)
    #
    if r.status_code == requests.codes.ok:
        return r.json
    else:
        return False


def _set(service_id, server_ip, server_port, self_ip, self_port):
    #
    data = {"id": service_id,
            "ipaddress": self_ip,
            "port": self_port}
    #
    server_url = _url(id, server_ip, server_port)
    #
    r = requests.post(server_url, body=data)
    #
    if r.status_code == requests.codes.ok:
        return True
    else:
        return False


def _url(service_id, server_ip, server_port):
    return 'http://{ipaddress}:{port}{uri}'.format(ipaddress=server_ip,
                                                   port=str(server_port),
                                                   uri=uri_configService.format(service_id=service_id))
