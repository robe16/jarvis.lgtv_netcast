from multiprocessing import Process
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from src.resources.global_resources.variables import jarvis_broadcastPort, jarvis_broadcast_msg
from src.discovery.broadcast import broadcast_service
from tests.broadcast.testlist import testlist


def discover_server():
    s = socket(AF_INET, SOCK_DGRAM) # create UDP socket
    s.bind(('', jarvis_broadcastPort))

    while True:
        data, addr = s.recvfrom(1024) # wait for a packet
        data = data.decode("utf-8")
        if data.startswith('jarvis'):
            return data


def my_ip():
    return gethostbyname(gethostname())


def run_test():
    for t in testlist:
        result = test_broadcast(t['service_id'], jarvis_broadcastPort)
        expect = jarvis_broadcast_msg.format(service_id=t['service_id'],
                                             service_type=t['service_type'],
                                             port=str(t['port']))
        result_compare(t['test_id'], expect, result, t['expected_result'])


def test_broadcast(service_id, port):
    process_test_broadcast = Process(target=broadcast_service, args=(service_id, port,))
    process_test_broadcast.start()
    result = discover_server()
    process_test_broadcast.terminate()
    return result


def result_compare(service_id, expect, result, expected_result):
    #
    r = True if result == expect else False
    str_result = 'PASS' if r == expected_result else 'FAIL'
    #
    print('Test #{id}::{str_result}::expected={expect}-v-result={result}'.format(id=service_id,
                                                                                 str_result=str_result,
                                                                                 expect=expect,
                                                                                 result=result))
