import sys
from multiprocessing import Process
from discovery.broadcast import broadcast_service
from portlistener import start_bottle
from lgtv_netcast.lgtv_netcast import tv_lg_netcast
from config.config import get_cfg_serviceid
from resources.global_resources.variables import *
from log.log import Log

_log = Log()


try:

    _log.new_entry(logCategoryProcess, '-', 'Starting micro service', '-', 'starting')

    ################################
    # Receive sys arguments

    # Argument 1: Port of self exposed on host
    try:
        self_hostport = sys.argv[1]
    except Exception as e:
        raise Exception('self_hostport not available - {e}'.format(e=e))

    ################################
    # As micro service will be containerised, a hard-coded port (1600) will be
    # used, and this will be mapped to as part of container build/deployment.
    self_port = 1600

    ################################
    # Initiate service broadcast

    process_test_broadcast = Process(target=broadcast_service, args=(get_cfg_serviceid, self_port,))
    process_test_broadcast.start()

    ################################
    # Create 'object'

    _device = tv_lg_netcast()

    _log.new_entry(logCategoryProcess, '-', 'Device object created',
                   'service_id-{service_id}.format(service_id=service_id)', 'success')

    ################################
    # Port_listener

    _log.new_entry(logCategoryProcess, '-', 'Port listener', 'port-{port}'.format(port=self_port), 'started')

    start_bottle(self_port, _device)

    process_test_broadcast.terminate()

    _log.new_entry(logCategoryProcess, '-', 'Port listener', '-'.format(port=self_port), 'stopped')

except Exception as e:
    print('An error has occurred starting micro service: {e}'.format(e=e))
    _log.new_entry(logCategoryProcess, '-', 'Starting micro service', e, 'fail', level=logLevelError)
