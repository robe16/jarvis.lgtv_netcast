from bottle import HTTPError
from bottle import get, post
from bottle import request, run, HTTPResponse

from resources.global_resources.variables import *
from config.config import get_cfg_serviceid, get_cfg_name, get_cfg_groups
from validation.validation import validate_command
from log.log import Log


def start_bottle(self_port, _device):

    _log = Log()

    ################################################################################################
    # Enable cross domain scripting
    ################################################################################################

    def enable_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        return response

    ################################################################################################
    # Groups
    ################################################################################################

    @get(uri_config)
    def get_info():
        try:
            #
            data = {'service_id': get_cfg_serviceid(),
                    'name': get_cfg_name(),
                    'groups': get_cfg_groups()}
            #
            status = httpStatusSuccess
            #
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelInfo)
            #
            return HTTPResponse(body=str(data), status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelError)
            raise HTTPError(status)

    ################################################################################################
    # Info
    ################################################################################################

    @get(uri_info)
    def get_info(resource_requested):
        try:
            #
            r = _device.getInfo(resource_requested)
            #
            if not bool(r):
                status = httpStatusFailure
            else:
                status = httpStatusSuccess
            #
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelInfo)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=str(r), status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelError)
            raise HTTPError(status)

    ################################################################################################
    # Commands
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
                    name = data_dict['executeApp']['name']
                    r = _device.executeApp(auid, name)
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
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'POST', status, level=logLevelInfo)
            #
            return HTTPResponse(status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'POST', status, level=logLevelError)
            raise HTTPError(status)

    ################################################################################################
    # Images
    ################################################################################################

    @get(uri_image)
    def get_image(auid, name):
        try:
            #
            r = _device.getImage(auid, name)
            #
            if not bool(r):
                status = httpStatusFailure
            else:
                status = httpStatusSuccess
            #
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelInfo)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=str(r), status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelError)
            raise HTTPError(status)

    ################################################################################################

    host='0.0.0.0'
    _log.new_entry(logCategoryProcess, '-', 'Port listener', '{host}:{port}'.format(host=host, port=self_port), 'started')
    run(host=host, port=self_port, debug=True)
