from socket import socket, AF_INET, SOCK_DGRAM
from resources.global_resources.variables import server_broadcastPort, server_broadcastCode
import datetime


def discover_server():
    s = socket(AF_INET, SOCK_DGRAM) # create UDP socket
    s.bind(('', server_broadcastPort))

    start_time = datetime.datetime.now()

    while start_time > (datetime.datetime.now() + datetime.timedelta(seconds = 20)):
        data, addr = s.recvfrom(1024) # wait for a packet
        data = data.decode("utf-8")
        if data.startswith(server_broadcastCode):
            return data[len(server_broadcastCode):]

    return False
