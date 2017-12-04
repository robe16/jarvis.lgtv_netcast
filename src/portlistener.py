from bottle import HTTPError
from bottle import get, post
from bottle import request, run, HTTPResponse

from tv_lg_netcast.tv_lg_netcast import TvLgNetcast
from resources.global_resources.variables import *
from config.config import get_cfg_serviceid, get_cfg_name_long, get_cfg_name_short, get_cfg_groups, get_cfg_subservices
from validation.validation import validate_keyInput, validate_executeApp
from log.log import log_inbound, log_internal


def start_bottle(self_port):

    ################################################################################################
    # Create device
    ################################################################################################

    _device = TvLgNetcast()

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
        #
        try:
            client = request.headers[service_header_clientid_label]
        except:
            client = request['REMOTE_ADDR']
        #
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
            log_inbound(False, client, request.url, 'GET', status)
            #
            return HTTPResponse(body=data, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, client, request.url, 'GET', status, exception=e)
            raise HTTPError(status)

    ################################################################################################
    # Apps (all and single)
    ################################################################################################

    @get(uri_apps_all)
    def get_apps_all():
        #
        try:
            client = request.headers[service_header_clientid_label]
        except:
            client = request['REMOTE_ADDR']
        #
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
            log_inbound(False, client, request.url, 'GET', status)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, client, request.url, 'GET', status, exception=e)
            raise HTTPError(status)

    ################################################################################################
    # Apps (all and single)
    ################################################################################################

    @get(uri_apps_single)
    def get_apps_single(auid):
        #
        try:
            client = request.headers[service_header_clientid_label]
        except:
            client = request['REMOTE_ADDR']
        #
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
            log_inbound(False, client, request.url, 'GET', status)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, client, request.url, 'GET', status, exception=e)
            raise HTTPError(status)

    ################################################################################################
    # Get commands
    ################################################################################################

    @get(uri_commands)
    def get_commands():
        #
        try:
            client = request.headers[service_header_clientid_label]
        except:
            client = request['REMOTE_ADDR']
        #
        try:
            #
            data = _device.getCommands()
            #
            status = httpStatusSuccess
            #
            log_inbound(False, client, request.url, 'GET', status)
            #
            return HTTPResponse(body=data, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, client, request.url, 'GET', status, exception=e)
            raise HTTPError(status)

    ################################################################################################
    # Post commands -
    ################################################################################################

    @post(uri_command_keyInput)
    def post_command_keyInput():
        #
        try:
            client = request.headers[service_header_clientid_label]
        except:
            client = request['REMOTE_ADDR']
        #
        try:
            #
            data_dict = request.json
            #
            if validate_keyInput(data_dict):
                #
                key = data_dict['keyInput']
                r = _device.sendCmd(key)
                #
                if not bool(r):
                    status = httpStatusFailure
                else:
                    status = httpStatusSuccess
            else:
                status = httpStatusBadrequest
            #
            log_inbound(False, client, request.url, 'POST', status, desc=request.json)
            #
            return HTTPResponse(status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, client, request.url, 'POST', status, desc=request.json, exception=e)
            raise HTTPError(status)

    ################################################################################################
    # Post commands
    ################################################################################################

    @post(uri_command_executeApp)
    def post_command_executeApp():
        #
        try:
            client = request.headers[service_header_clientid_label]
        except:
            client = request['REMOTE_ADDR']
        #
        try:
            #
            data_dict = request.json
            #
            if validate_executeApp(data_dict):
                #
                auid = data_dict['executeApp']
                r = _device.executeApp(auid)
                #
                if not bool(r):
                    status = httpStatusFailure
                else:
                    status = httpStatusSuccess
            else:
                status = httpStatusBadrequest
            #
            log_inbound(False, client, request.url, 'POST', status, desc=request.json)
            #
            return HTTPResponse(status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, client, request.url, 'POST', status, desc=request.json, exception=e)
            raise HTTPError(status)

    ################################################################################################
    # Images
    ################################################################################################

    @get(uri_image_appicon)
    def get_image_appicon(auid):
        #
        try:
            client = request.headers[service_header_clientid_label]
        except:
            client = request['REMOTE_ADDR']
        #
        try:
            #
            r = _device.getImage_app(auid)
            #
            if not bool(r):
                status = httpStatusFailure
            else:
                status = httpStatusSuccess
            #
            log_inbound(False, client, request.url, 'GET', status)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            log_inbound(False, client, request.url, 'GET', status, exception=e)
            raise HTTPError(status)

    ################################################################################################

    host='0.0.0.0'
    log_internal(True, 'Port listener', desc='started')
    run(host=host, port=self_port, debug=True)
