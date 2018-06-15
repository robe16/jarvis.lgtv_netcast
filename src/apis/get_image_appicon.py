from bottle import HTTPResponse, HTTPError

from common_functions.request_enable_cors import enable_cors
from common_functions.request_log_args import get_request_log_args
from log.log import log_inbound
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.global_resources.variables import *


def get_image_appicon(request, _tvlgnetcast, auid):
    #
    args = get_request_log_args(request)
    #
    try:
        #
        r = _tvlgnetcast.getImage_app(auid)
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
        response = HTTPResponse()
        response.status = status
        enable_cors(response)
        #
        if not isinstance(r, bool):
            response.body = r
        #
        return response
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
