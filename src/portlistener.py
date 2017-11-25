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
    # Service info & Groups
    ################################################################################################

    @get(uri_config)
    def get_config():
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
            return HTTPResponse(body=data, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelError)
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
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelInfo)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelError)
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
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelInfo)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelError)
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
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelInfo)
            #
            return HTTPResponse(body=data, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelError)
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
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelInfo)
            #
            if isinstance(r, bool):
                return HTTPResponse(status=status)
            else:
                return HTTPResponse(body=r, status=status)
            #
        except Exception as e:
            status = httpStatusServererror
            _log.new_entry(logCategoryClient, request['REMOTE_ADDR'], request.url, 'GET', status, level=logLevelError)
            raise HTTPError(status)

    ################################################################################################

    host='0.0.0.0'
    _log.new_entry(logCategoryProcess, '-', 'Port listener', '{host}:{port}'.format(host=host, port=self_port), 'started')
    run(host=host, port=self_port, debug=True)
