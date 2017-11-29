from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from parameters import broadcast_frequency
from resources.global_resources.variables import *
from log.log import log_internal


def broadcast_service(service_id, self_port):
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('0.0.0.0', 0))
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        #
        msg = jarvis_broadcast_msg.format(service_id=service_id,
                                          service_type=serviceType,
                                          port=str(self_port))
        #
        while True:
            s.sendto(msg, ('<broadcast>', jarvis_broadcastPort))
            sleep(broadcast_frequency)
        #
    except Exception as e:
        log_internal(True, 'Broadcasting service', desc='fail', exception=e)
