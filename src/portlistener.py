import os
from bottle import HTTPError
from bottle import get, post
from bottle import request, run, static_file, HTTPResponse

# from lists.resources.english import *
from resources.global_resources.variables import uri_info, uri_command
from log.log import *


def start_bottle(self_port):
    #
    run_bottle(self_port)

################################################################################################
# Enable cross domain scripting
################################################################################################

def enable_cors(response):
    #
    # Wildcard '*' for Access-Control-Allow-Origin as mirrorUI will be hosted in 'file://' on device
    #
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    # response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    #
    return response

################################################################################################
# Create log message
################################################################################################

def log_msg(request, resource):
    #
    ip = request['REMOTE_ADDR']
    msg = '{ip} - {resource}'.format(ip=ip, resource=resource)
    #
    return msg

################################################################################################

@get(uri_info)
def getInfo(resource_requested=False):
    pass


@post(uri_command)
def getInfo():
    pass

################################################################################################
# Handle requests for resource data
################################################################################################


@get(uri_data_device)
def get_data_device(group=False, thing=False, resource_requested=False):
    #
    log = log_msg(request, uri_data_device)
    #
    try:
        #
        if (not group) or (not thing) or (not resource_requested):
            log_error('{log} - {error}'.format(log=log, error='URI invalid'))
            raise HTTPError(404)
        #
        try:
            group_seq = get_cfg_group_seq(group)
            thing_seq = get_cfg_thing_seq(group, thing)
        except Exception as e:
            log_error('{log} - {error}'.format(log=log, error=e))
            raise HTTPError(404)
        #
        data_dict = {'data': resource_requested}
        #
        rsp = devices[group_seq][thing_seq].getData(data_dict)
        #
        log_general(log)
        #
        if isinstance(rsp, bool):
            return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
        else:
            return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
        #
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        raise HTTPError(500)


################################################################################################
# Handle commands
################################################################################################

@post(uri_command_device)
def send_command_device(group=False, thing=False):
    #
    global devices
    #
    log = log_msg(request, uri_command_device)
    #
    try:
        #
        if (not group) or (not thing):
            log_error('{log} - {error}'.format(log=log, error='URI invalid'))
            raise HTTPError(404)
        #
        try:
            group_seq = get_cfg_group_seq(group)
            thing_seq = get_cfg_thing_seq(group, thing)
        except Exception as e:
            log_error('{log} - {error}'.format(log=log, error=e))
            raise HTTPError(404)
        #
        cmd_dict = request.json
        #
        rsp = devices[group_seq][thing_seq].sendCmd(cmd_dict)
        #
        log_general(log)
        #
        if isinstance(rsp, bool):
            return HTTPResponse(status=200) if rsp else HTTPResponse(status=400)
        else:
            return HTTPResponse(body=str(rsp), status=200) if bool(rsp) else HTTPResponse(status=400)
        #
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        raise HTTPError(500)


################################################################################################
# Image files
################################################################################################


@get(uri_image)
def get_image(category, filename):
    log = log_msg(request, uri_image)
    try:
        root = os.path.join(os.path.dirname(__file__), 'imgs/{img_cat}'.format(img_cat=category))
        mimetype = filename.split('.')[1]
        log_general(log)
        return static_file(filename, root=root, mimetype='image/{mimetype}'.format(mimetype=mimetype))
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        raise HTTPError(500)

################################################################################################

def run_bottle(self_port):
    host='0.0.0.0'
    log_general('Bottle started: listening on {host}:{port}'.format(host=host, port=self_port))
    run(host=host, port=self_port, debug=True)
