import sys
from portlistener import start_bottle

from lgtv_netcast.lgtv_netcast import tv_lg_netcast
from resources.global_resources.variables import *
from log.log import Log

_log = Log()

################################
# Receive sys arguments
################################
# First argument passed through is the
# port the application listens on
try:
    self_port = sys.argv[1]
except:
    self_port = 1600  # default port
#
################################
# Create 'object'
################################
#
_log.new_entry(logCategoryProcess, '-', 'Getting data from config server', '-', 'started')
#
# TODO - get ipaddress, port, pairingkey from server
#
ipaddress = ''
port = ''
pairingkey = ''
#
_log.new_entry(logCategoryProcess, '-', 'Config info received from server', 'ipaddress-{ip}'.format(ip=ipaddress), '-')
_log.new_entry(logCategoryProcess, '-', 'Config info received from server', 'port-{port}'.format(port=port), '-')
_log.new_entry(logCategoryProcess, '-', 'Config info received from server', 'pairingkey-{pairingkey}'.format(pairingkey=pairingkey), '-')
#
_device = tv_lg_netcast(ipaddress, port, pairingkey)
#
_log.new_entry(logCategoryProcess, '-', 'Getting data from config server', '-', 'started')
#
################################
# Port_listener
################################
#
_log.new_entry(logCategoryProcess, '-', 'Port listener', 'port-{port}'.format(port=self_port), 'started')
#
start_bottle(self_port, _device)
#
_log.new_entry(logCategoryProcess, '-', 'Port listener', '-'.format(port=self_port), 'stopped')