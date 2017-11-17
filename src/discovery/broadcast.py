from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from parameters import broadcast_frequency
from resources.global_resources.variables import serviceType, jarvis_broadcastFromPort, jarvis_broadcastPort, \
    jarvis_broadcast_msg


def broadcast_service(service_id, host_port, self_broadcastPort):
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('0.0.0.0', jarvis_broadcastFromPort))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    msg = jarvis_broadcast_msg.format(service_id=service_id,
                                      service_type=serviceType,
                                      port=str(host_port))

    while True:
        s.sendto(msg, ('<broadcast>', jarvis_broadcastPort))
        sleep(broadcast_frequency)
