import threading
from bottle import get, post
from bottle import request, run

from service.tv_lg_netcast import TvLgNetcast
from resources.lang.enGB.logs import *
from resources.global_resources.log_vars import logPass
from config.config import get_cfg_port_listener
from log.log import log_internal

from apis.get_config import get_config
from apis.get_apps_all import get_apps_all
from apis.get_apps_single import get_apps_single
from apis.get_commands import get_commands
from apis.post_command_keyInput import post_command_keyInput
from apis.post_command_executeApp import post_command_executeApp
from apis.post_command_cursorVisbility import post_command_cursorVisbility
from apis.post_command_touchMove import post_command_touchMove
from apis.post_command_touchClick import post_command_touchClick
from apis.post_command_touchWheel import post_command_touchWheel
from apis.get_volume import get_volume
from apis.get_3d import get_3d
from apis.get_image_screenshot import get_image_screenshot
from apis.get_image_appicon import get_image_appicon


def start_bottle(port_threads):

    ################################################################################################
    # Create device
    ################################################################################################

    _tvlgnetcast = TvLgNetcast()

    log_internal(logPass, logDescDeviceObjectCreation, description='success')

    ################################################################################################
    # APIs
    ################################################################################################

    @get('/config')
    def api_get_config():
        return get_config(request)

    @get('/apps/all')
    def api_get_apps_all():
        return get_apps_all(request, _tvlgnetcast)

    @get('/apps/single/<auid>')
    def api_get_apps_single(auid):
        return get_apps_single(request, _tvlgnetcast, auid)

    @get('/commands')
    def api_get_commands():
        return get_commands(request, _tvlgnetcast)

    @post('/command/keyInput')
    def api_post_command_keyInput():
        return post_command_keyInput(request, _tvlgnetcast)

    @post('/command/executeApp')
    def api_post_command_executeApp():
        return post_command_executeApp(request, _tvlgnetcast)

    @post('/command/cursor/visibility')
    def api_post_command_cursorVisbility():
        return post_command_cursorVisbility(request, _tvlgnetcast)

    @post('/command/touch/move')
    def api_post_command_touchMove():
        return post_command_touchMove(request, _tvlgnetcast)

    @post('/command/touch/click')
    def api_post_command_touchClick():
        return post_command_touchClick(request, _tvlgnetcast)

    @post('/command/touch/wheel')
    def api_post_command_touchWheel():
        return post_command_touchWheel(request, _tvlgnetcast)

    @get('/volume')
    def api_get_volume():
        return get_volume(request, _tvlgnetcast)

    @get('/3d')
    def api_get_3d():
        return get_3d(request, _tvlgnetcast)

    @get('/img/screenshot')
    def api_get_image_screenshot():
        return get_image_screenshot(request, _tvlgnetcast)

    @get('/img/appicon/<auid>')
    def api_get_image_appicon(auid):
        return get_image_appicon(request, _tvlgnetcast, auid)


    ################################################################################################

    def bottle_run(x_host, x_port):
        log_internal(logPass, logDescPortListener.format(port=x_port), description='started')
        run(host=x_host, port=x_port, debug=True)

    ################################################################################################

    host = 'localhost'
    ports = get_cfg_port_listener()
    for port in ports:
        t = threading.Thread(target=bottle_run, args=(host, port,))
        port_threads.append(t)

    # Start all threads
    for t in port_threads:
        t.start()
    # Use .join() for all threads to keep main process 'alive'
    for t in port_threads:
        t.join()
