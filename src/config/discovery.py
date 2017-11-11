from socket import socket, AF_INET, SOCK_DGRAM
from resources.global_resources.variables import server_broadcastPort, server_broadcastCode


def discover_server():
    s = socket(AF_INET, SOCK_DGRAM) # create UDP socket
    s.bind(('', server_broadcastPort))

    while True:
        data, addr = s.recvfrom(1024) # wait for a packet
        if data.startswith(server_broadcastCode):
            return data[len(server_broadcastCode):]
