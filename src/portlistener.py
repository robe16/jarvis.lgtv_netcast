from bottle import HTTPError
from bottle import get, post
from bottle import request, run, HTTPResponse

from lgtv_netcast.lgtv_netcast import tv_lg_netcast
from resources.global_resources.variables import *
from config.config import get_cfg_serviceid, get_cfg_name_long, get_cfg_name_short, get_cfg_groups, get_cfg_subservices
from validation.validation import validate_command
from log.log import log_inbound, log_internal


def start_bottle(self_port):

    ################################################################################################
    # Create device
    ################################################################################################

    _device = tv_lg_netcast()

    log_internal(True, 'Device object created', desc='success')

    ################################################################################################
    # Enable cross domain scripting
    ################################################################################################

    def enable_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        return response

    ################################################################################################
    # Service info & Groups
    ################################################################################################

    @get(uri_config)
    def get_config():
        try:
            #
            data = {'service_id': get_cfg_serviceid(),
                    'name_long': get_cfg_name_long(),
                    'name_short': get_cfg_name_short(),
                    'subservices': get_cfg_subservices(),
                    'groups': get_cfg_groups()}
            #
            status = httpStatusSuccess
            #
            log_inbound(False, request['REMOTE_ADDR'], request.url, 'GET', status)
            #
            return HTTPResponse(body=data, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, request['REMOTE_ADDR'], request.url, 'GET', status, exception=e)
            raise HTTPError(status)

    ################################################################################################
    # Apps (all and single)
    ################################################################################################

    @get(uri_apps_all)
    def get_apps_all():
        try:
            #
            r = _device.getApps_all()
            #
            # Add URI for retrieving image item
            for k in r.keys():
                r[k]['image'] = format_uri_image_appicon.format(auid=r[k]['auid'])
            #
            if not bool(r):
                status = httpStatusFailure
            else:
                status = httpStatusSuccess
            #
            log_inbound(False, request['REMOTE_ADDR'], request.url, 'GET', status)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, request['REMOTE_ADDR'], request.url, 'GET', status, exception=e)
            raise HTTPError(status)

    ################################################################################################
    # Apps (all and single)
    ################################################################################################

    @get(uri_apps_single)
    def get_apps_single(auid):
        try:
            #
            r = _device.getApps_single(auid)
            #
            # Add URI for retrieving image item
            r['image'] = format_uri_image_appicon.format(auid=r['auid'])
            #
            if not bool(r):
                status = httpStatusFailure
            else:
                status = httpStatusSuccess
            #
            log_inbound(False, request['REMOTE_ADDR'], request.url, 'GET', status)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, request['REMOTE_ADDR'], request.url, 'GET', status, exception=e)
            raise HTTPError(status)

    ################################################################################################
    # Get commands
    ################################################################################################

    @get(uri_commands)
    def get_commands():
        try:
            #
            data = _device.getCommands()
            #
            status = httpStatusSuccess
            #
            log_inbound(False, request['REMOTE_ADDR'], request.url, 'GET', status)
            #
            return HTTPResponse(body=data, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, request['REMOTE_ADDR'], request.url, 'GET', status, exception=e)
            raise HTTPError(status)

    ################################################################################################
    # Post commands
    ################################################################################################

    @post(uri_command)
    def post_command():
        try:
            #
            data_dict = request.json
            #
            if validate_command(data_dict):
                #
                if data_dict['command'] == 'keyInput':
                    key = data_dict['keyInput']['key']
                    r = _device.sendCmd(key)
                elif data_dict['command'] == 'executeApp':
                    auid = data_dict['executeApp']['auid']
                    r = _device.executeApp(auid)
                else:
                    raise Exception('')
                #
                if not bool(r):
                    status = httpStatusFailure
                else:
                    status = httpStatusSuccess
            else:
                status = httpStatusBadrequest
            #
            log_inbound(False, request['REMOTE_ADDR'], request.url, 'POST', status, desc=request.query)
            #
            return HTTPResponse(status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, request['REMOTE_ADDR'], request.url, 'POST', status, desc=request.query, exception=e)
            raise HTTPError(status)

    ################################################################################################
    # Images
    ################################################################################################

    @get(uri_image_appicon)
    def get_image_appicon(auid):
        try:
            #
            r = _device.getImage_app(auid)
            #
            if not bool(r):
                status = httpStatusFailure
            else:
                status = httpStatusSuccess
            #
            log_inbound(False, request['REMOTE_ADDR'], request.url, 'GET', status)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, request['REMOTE_ADDR'], request.url, 'GET', status, exception=e)
            raise HTTPError(status)

    ################################################################################################

    host='0.0.0.0'
    log_internal(True, 'Port listener', desc='started')
    run(host=host, port=self_port, debug=True)
