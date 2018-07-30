from bottle import request, run, route, get, post

from config.config import get_cfg_port
from common_functions.request_enable_cors import response_options
from service.tv_lg_netcast import TvLgNetcast
from resources.lang.enGB.logs import *
from resources.global_resources.log_vars import logPass
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


def start_bottle():

    ################################################################################################
    # Create device
    ################################################################################################

    _tvlgnetcast = TvLgNetcast()

    log_internal(logPass, logDescDeviceObjectCreation, description='success')

    ################################################################################################
    # APIs
    ################################################################################################

    @route('/config', method=['OPTIONS'])
    @route('/apps/all', method=['OPTIONS'])
    @route('/apps/single/<auid>', method=['OPTIONS'])
    @route('/commands', method=['OPTIONS'])
    @route('/command/<command>', method=['OPTIONS'])
    @route('/command/cursor/<command>', method=['OPTIONS'])
    @route('/command/touch/<command>', method=['OPTIONS'])
    @route('/volume', method=['OPTIONS'])
    @route('/3d', method=['OPTIONS'])
    @route('/img/screenshot', method=['OPTIONS'])
    @route('/img/appicon/<auid>', method=['OPTIONS'])
    def api_cors_options(**kwargs):
        return response_options()

    @get('/config')
    def api_get_config():
        response = get_config(request)
        return response

    @get('/apps/all')
    def api_get_apps_all():
        response = get_apps_all(request, _tvlgnetcast)
        return response

    @get('/apps/single/<auid>')
    def api_get_apps_single(auid):
        response = get_apps_single(request, _tvlgnetcast, auid)
        return response

    @get('/commands')
    def api_get_commands():
        response = get_commands(request, _tvlgnetcast)
        return response

    @post('/command/keyInput')
    def api_post_command_keyInput():
        response = post_command_keyInput(request, _tvlgnetcast)
        return response

    @post('/command/executeApp')
    def api_post_command_executeApp():
        response = post_command_executeApp(request, _tvlgnetcast)
        return response

    @post('/command/cursor/visibility')
    def api_post_command_cursorVisbility():
        response = post_command_cursorVisbility(request, _tvlgnetcast)
        return response

    @post('/command/touch/move')
    def api_post_command_touchMove():
        response = post_command_touchMove(request, _tvlgnetcast)
        return response

    @post('/command/touch/click')
    def api_post_command_touchClick():
        response = post_command_touchClick(request, _tvlgnetcast)
        return response

    @post('/command/touch/wheel')
    def api_post_command_touchWheel():
        response = post_command_touchWheel(request, _tvlgnetcast)
        return response

    @get('/volume')
    def api_get_volume():
        response = get_volume(request, _tvlgnetcast)
        return response

    @get('/3d')
    def api_get_3d():
        response = get_3d(request, _tvlgnetcast)
        return response

    @get('/img/screenshot')
    def api_get_image_screenshot():
        response = get_image_screenshot(request, _tvlgnetcast)
        return response

    @get('/img/appicon/<auid>')
    def api_get_image_appicon(auid):
        response = get_image_appicon(request, _tvlgnetcast, auid)
        return response


    ################################################################################################

    host = '0.0.0.0'
    port = get_cfg_port()
    run(host=host, port=port, server='paste', debug=True)

    log_internal(logPass, logDescPortListener.format(port=port), description='started')

    ################################################################################################
