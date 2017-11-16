from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from parameters import broadcast_frequency
from resources.global_resources.variables import serviceType, jarvis_broadcastPort, jarvis_broadcast_msg


def broadcast_service(service_id, host_port):
    s = socket(AF_INET, SOCK_DGRAM)  # create UDP socket
    s.bind(('0.0.0.0', 0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # this is a broadcast socket

    msg = jarvis_broadcast_msg.format(service_id=service_id,
                                      service_type=serviceType,
                                      port=str(host_port))

    while True:
        s.sendto(msg, ('<broadcast>', jarvis_broadcastPort))
        sleep(broadcast_frequency)

broadcast_service('test', '0000')