from datetime import datetime
import logging
import os

from config.config import get_cfg_serviceid
from resources.global_resources.variables import serviceType, timeformat
from resources.global_resources.variables import logPass, logFail, logException
from resources.global_resources.variables import logMsg_Inbound_Info, logMsg_Inbound_Error
from resources.global_resources.variables import logMsg_Internal_Info, logMsg_Internal_Error
from resources.global_resources.variables import logMsg_Outbound_Info, logMsg_Outbound_Error


def log_inbound(result, client, uri, method, httpresponse, desc='-', exception=False):
    #
    if exception:
        result = logException
        log_msg = logMsg_Inbound_Error.format(timestamp=_timestamp(),
                                              serviceid=get_cfg_serviceid(),
                                              servicetype=serviceType,
                                              result=result,
                                              exception=exception,
                                              client=client,
                                              uri=uri,
                                              method=method,
                                              httpresponse=httpresponse,
                                              desc=desc)
        level = 40
    else:
        result = logPass if result else logFail
        log_msg = logMsg_Inbound_Info.format(timestamp=_timestamp(),
                                             serviceid=get_cfg_serviceid(),
                                             servicetype=serviceType,
                                             result=result,
                                             client=client,
                                             uri=uri,
                                             method=method,
                                             httpresponse=httpresponse,
                                             desc=desc)
        level = 20
    #
    _log(log_msg, level)


def log_internal(result, operation, desc='-', exception=False):
    #
    if exception:
        result = logException
        log_msg = logMsg_Internal_Error.format(timestamp=_timestamp(),
                                               serviceid=get_cfg_serviceid(),
                                               servicetype=serviceType,
                                               result=result,
                                               exception=exception,
                                               operation=operation,
                                               desc=desc)
        level = 40
    else:
        result = logPass if result else logFail
        log_msg = logMsg_Internal_Info.format(timestamp=_timestamp(),
                                              serviceid=get_cfg_serviceid(),
                                              servicetype=serviceType,
                                              result=result,
                                              operation=operation,
                                              desc=desc)
        level = 20
    #
    _log(log_msg, level)


def log_outbound(result, ip, uri, method, httpresponse, desc='-', exception=False):
    #
    if exception:
        result = logException
        log_msg = logMsg_Outbound_Error.format(timestamp=_timestamp(),
                                               serviceid=get_cfg_serviceid(),
                                               servicetype=serviceType,
                                               result=result,
                                               exception=exception,
                                               ip=ip,
                                               uri=uri,
                                               method=method,
                                               httpresponse=httpresponse,
                                               desc=desc)
        level = 40
    else:
        result = logPass if result else logFail
        log_msg = logMsg_Outbound_Info.format(timestamp=_timestamp(),
                                              serviceid=get_cfg_serviceid(),
                                              servicetype=serviceType,
                                              result=result,
                                              ip=ip,
                                              uri=uri,
                                              method=method,
                                              httpresponse=httpresponse,
                                              desc=desc)
        level = 20
    #
    _log(log_msg, level)


def _log(log_msg, level):
    #
    if level == 50:
        logging.critical(log_msg)
    elif level == 40:
        logging.error(log_msg)
    elif level == 30:
        logging.warning(log_msg)
    elif level == 20:
        logging.info(log_msg)
    else:
        logging.debug(log_msg)


def set_logfile():
    filename = '{filename}.log'.format(filename=get_cfg_serviceid())
    logfile = os.path.join(os.path.dirname(__file__), 'logfiles', filename)
    logging.basicConfig(filename=logfile, level=20)


def _timestamp():
    return datetime.now().strftime(timeformat)