from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
from parameters import broadcast_frequency
from resources.global_resources.variables import serviceType, jarvis_broadcastPort, jarvis_broadcast_msg


def broadcast_service(service_id, host_port):
    s = socket(AF_INET, SOCK_DGRAM)  # create UDP socket
    s.bind(('', 0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # this is a broadcast socket

    msg = jarvis_broadcast_msg.format(service_id=service_id,
                                      service_type=serviceType,
                                      host=gethostbyname(gethostname()),
                                      port=str(host_port))

    while True:
        data = bytes(msg, "utf-8")
        s.sendto(data, ('<broadcast>', jarvis_broadcastPort))
        sleep(broadcast_frequency)


# TODO - sample code for clients to discover service
# def discover_service():
#     s = socket(AF_INET, SOCK_DGRAM) # create UDP socket
#     s.bind(('', jarvis_broadcastPort))
#
#     while True:
#         data, addr = s.recvfrom(1024) # wait for a packet
#         data = data.decode("utf-8")
#         if data.startswith('jarvis'):
#             data = data.split('::')
#             #
#             d = {'service_id': data[1],
#                  'service_type': data[2],
#                  'url': data[3]}
#             #
#             return d