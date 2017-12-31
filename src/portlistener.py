import threading
from bottle import HTTPError
from bottle import get, post
from bottle import request, run, HTTPResponse

from tv_lg_netcast.tv_lg_netcast import TvLgNetcast
from common_functions.query_to_string import convert_query_to_string
from resources.global_resources.variables import *
from resources.lang.enGB.logs import *
from resources.global_resources.log_vars import logPass, logFail, logException
from config.config import get_cfg_serviceid, get_cfg_name_long, get_cfg_name_short, get_cfg_groups, get_cfg_subservices
from config.config import get_cfg_port_listener
from validation.validation import validate_keyInput, validate_executeApp
from log.log import log_inbound, log_internal


def start_bottle(port_threads):

    ################################################################################################
    # Create device
    ################################################################################################

    _device = TvLgNetcast()

    log_internal(logPass, logDescDeviceObjectCreation, description='success')

    ################################################################################################
    # Enable cross domain scripting
    ################################################################################################

    def enable_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        return response

    ################################################################################################
    # Log arguments
    ################################################################################################

    def _get_log_args(request):
        #
        urlparts = request.urlparts
        #
        try:
            client_ip = request.headers['X-Forwarded-For']
        except:
            client_ip = request['REMOTE_ADDR']
        #
        try:
            server_ip = request.headers['X-Real-IP']
        except:
            server_ip = urlparts.hostname
        #
        try:
            client_user = request.headers[service_header_clientid_label]
        except:
            client_user = request['REMOTE_ADDR']
        #
        server_request_query = convert_query_to_string(request.query) if request.query_string else '-'
        server_request_body = request.body.read() if request.body.read()!='' else '-'
        #
        return {'client_ip': client_ip,
                'client_user': client_user,
                'server_ip': server_ip,
                'server_thread_port': urlparts.port,
                'server_method': request.method,
                'server_request_uri': urlparts.path,
                'server_request_query': server_request_query,
                'server_request_body': server_request_body}

    ################################################################################################
    # Service info & Groups
    ################################################################################################

    @get(uri_config)
    def get_config():
        #
        args = _get_log_args(request)
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
            args['result'] = logPass
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
            #
            return HTTPResponse(body=data, status=status)
            #
        except Exception as e:
            #
            status = httpStatusServererror
            #
            args['result'] = logException
            args['http_response_code'] = status
            args['description'] = '-'
            args['exception'] = e
            log_inbound(**args)
            #
            raise HTTPError(status)

    ################################################################################################
    # Apps (all and single)
    ################################################################################################

    @get(uri_apps_all)
    def get_apps_all():
        #
        args = _get_log_args(request)
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
                result = logFail
            else:
                status = httpStatusSuccess
                result = logPass
            #
            args['result'] = result
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            #
            status = httpStatusServererror
            #
            args['result'] = logException
            args['http_response_code'] = status
            args['description'] = '-'
            args['exception'] = e
            log_inbound(**args)
            #
            raise HTTPError(status)

    ################################################################################################
    # Apps (all and single)
    ################################################################################################

    @get(uri_apps_single)
    def get_apps_single(auid):
        #
        args = _get_log_args(request)
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
                result = logFail
            else:
                status = httpStatusSuccess
                result = logPass
            #
            args['result'] = result
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            #
            status = httpStatusServererror
            #
            args['result'] = logException
            args['http_response_code'] = status
            args['description'] = '-'
            args['exception'] = e
            log_inbound(**args)
            #
            raise HTTPError(status)

    ################################################################################################
    # Get commands
    ################################################################################################

    @get(uri_commands)
    def get_commands():
        #
        args = _get_log_args(request)
        #
        try:
            #
            data = _device.getCommands()
            #
            status = httpStatusSuccess
            #
            args['result'] = logPass
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
            #
            return HTTPResponse(body=data, status=status)
            #
        except Exception as e:
            #
            status = httpStatusServererror
            #
            args['result'] = logException
            args['http_response_code'] = status
            args['description'] = '-'
            args['exception'] = e
            log_inbound(**args)
            #
            raise HTTPError(status)

    ################################################################################################
    # Post commands - keyInput
    ################################################################################################

    @post(uri_command_keyInput)
    def post_command_keyInput():
        #
        args = _get_log_args(request)
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
                    result = logFail
                else:
                    status = httpStatusSuccess
                    result = logPass
            else:
                status = httpStatusBadrequest
                result = logFail
            #
            args['result'] = result
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
            #
            return HTTPResponse(status=status)
            #
        except Exception as e:
            #
            status = httpStatusServererror
            #
            args['result'] = logException
            args['http_response_code'] = status
            args['description'] = '-'
            args['exception'] = e
            log_inbound(**args)
            #
            raise HTTPError(status)

    ################################################################################################
    # Post commands - executeApp
    ################################################################################################

    @post(uri_command_executeApp)
    def post_command_executeApp():
        #
        args = _get_log_args(request)
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
                    result = logFail
                else:
                    status = httpStatusSuccess
                    result = logPass
            else:
                status = httpStatusBadrequest
                result = logFail
            #
            args['result'] = result
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
            #
            return HTTPResponse(status=status)
            #
        except Exception as e:
            #
            status = httpStatusServererror
            #
            args['result'] = logException
            args['http_response_code'] = status
            args['description'] = '-'
            args['exception'] = e
            log_inbound(**args)
            #
            raise HTTPError(status)

    ################################################################################################
    # Get volume
    ################################################################################################

    @get(uri_volume)
    def get_volume():
        #
        args = _get_log_args(request)
        #
        try:
            #
            r = _device.getVolume()
            #
            if not bool(r):
                status = httpStatusFailure
                result = logFail
            else:
                status = httpStatusSuccess
                result = logPass
            #
            args['result'] = result
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            #
            status = httpStatusServererror
            #
            args['result'] = logException
            args['http_response_code'] = status
            args['description'] = '-'
            args['exception'] = e
            log_inbound(**args)
            #
            raise HTTPError(status)

    ################################################################################################
    # Get 3D status
    ################################################################################################

    @get(uri_volume)
    def get_volume():
        #
        args = _get_log_args(request)
        #
        try:
            #
            r = _device.get3d()
            #
            if not bool(r):
                status = httpStatusFailure
                result = logFail
            else:
                status = httpStatusSuccess
                result = logPass
            #
            args['result'] = result
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            #
            status = httpStatusServererror
            #
            args['result'] = logException
            args['http_response_code'] = status
            args['description'] = '-'
            args['exception'] = e
            log_inbound(**args)
            #
            raise HTTPError(status)

    ################################################################################################
    # Screenshot
    ################################################################################################

    @get(uri_image_screenshot)
    def get_image_screenshot():
        #
        args = _get_log_args(request)
        #
        try:
            #
            r = _device.getImage_screenshot()
            #
            if not bool(r):
                status = httpStatusFailure
                result = logFail
            else:
                status = httpStatusSuccess
                result = logPass
            #
            args['result'] = result
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            #
            status = httpStatusServererror
            #
            args['result'] = logException
            args['http_response_code'] = status
            args['description'] = '-'
            args['exception'] = e
            log_inbound(**args)
            #
            raise HTTPError(status)

    ################################################################################################
    # Images
    ################################################################################################

    @get(uri_image_appicon)
    def get_image_appicon(auid):
        #
        args = _get_log_args(request)
        #
        try:
            #
            r = _device.getImage_app(auid)
            #
            if not bool(r):
                status = httpStatusFailure
                result = logFail
            else:
                status = httpStatusSuccess
                result = logPass
            #
            args['result'] = result
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            #
            status = httpStatusServererror
            #
            args['result'] = logException
            args['http_response_code'] = status
            args['description'] = '-'
            args['exception'] = e
            log_inbound(**args)
            #
            raise HTTPError(status)

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
