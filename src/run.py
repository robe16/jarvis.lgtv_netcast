import sys
from portlistener import start_bottle
from config.getconfig import get_config
from lgtv_netcast.lgtv_netcast import tv_lg_netcast
from resources.global_resources.variables import *
from log.log import Log

_log = Log()


try:

    _log.new_entry(logCategoryProcess, '-', 'Starting micro service', '-', 'starting')

    ################################
    # Receive sys arguments

    # Argument 1: Device id that correlates to config file
    try:
        service_id = sys.argv[1]
    except:
        raise Exception('service_id not available')

    # Argument 2: IP address of the config server
    try:
        server_ip = sys.argv[2]
    except:
        raise Exception('server_ip not available')

    # Argument 3: Port number of the config server
    try:
        server_port = sys.argv[3]
    except:
        raise Exception('server_port not available')

    ################################
    # As micro service will be containerised, a hard-coded port (1600) will be
    # used, and this will be mapped to as part of container build/deployment.
    self_port = 1600

    self_ip = ''

    ################################
    # Get info from server

    _log.new_entry(logCategoryProcess, '-', 'Getting data from config server', '-', 'started')

    config = get_config(service_id, server_ip, server_port, self_ip, self_port)

    if not bool(config):
        raise Exception('Config data not available')

    ipaddress = config['ipaddress']
    port = config['port']
    pairingkey = config['pairingkey']

    _log.new_entry(logCategoryProcess, '-', 'Config info received from server', 'ipaddress-{ip}'.format(ip=ipaddress), '-')
    _log.new_entry(logCategoryProcess, '-', 'Config info received from server', 'port-{port}'.format(port=port), '-')
    _log.new_entry(logCategoryProcess, '-', 'Config info received from server', 'pairingkey-{pairingkey}'.format(pairingkey=pairingkey), '-')

    ################################
    # Create 'object'

    _device = tv_lg_netcast(ipaddress, port, pairingkey)

    _log.new_entry(logCategoryProcess, '-', 'Device object created', 'id-{id}.format(id=id)', 'success')

    ################################
    # Port_listener

    _log.new_entry(logCategoryProcess, '-', 'Port listener', 'port-{port}'.format(port=self_port), 'started')

    start_bottle(self_port, _device)

    _log.new_entry(logCategoryProcess, '-', 'Port listener', '-'.format(port=self_port), 'stopped')

except Exception as e:
    _log.new_entry(logCategoryProcess, '-', 'Starting micro service', e, 'fail', level=logLevelError)
