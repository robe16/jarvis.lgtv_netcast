from datetime import datetime
import logging
import schedule
import os

from resources.global_resources.variables import timeformat
from resources.global_resources.variables import logFileName, logFileNameTimeformat
from resources.global_resources.variables import logLevelInfo, logLevelWarning, logLevelError, logLevelCritical

# Logging Level Values:
#  CRITICAL 50
#  ERROR    40
#  WARNING  30
#  INFO     20
#  DEBUG    10
#  UNSET     0

# Log entry template:
# LEVEL:user::%Y/%m/%d %H.%M.%S.%f::description-1::description-2::outcome
#
# NOTE: delimiter-separated value - '::'

# Example log entries:
# INFO:root::2017/01/01 01:36:38.352956::/command::POST::200
# WARNING:root::2017/01/01 01:36:38.352956::/info::GET::404
# ERROR:root::2017/01/01 01:36:38.352956::/info::GET::500
# INFO:root::2017/01/01 01:36:38.352956::Device::TV Apps list retrieval::success
# ERROR:root::2017/01/01 01:36:38.352956::Pairing device::/udap/api/pairing::connection timeout


class Log():

    def __init__(self):
        self._set_logfile()
        schedule.every().day.at("00:00").do(self._set_logfile)

    def _set_logfile(self):
        filename = '{timestamp} {filename}.log'.format(timestamp = logFileNameTimeformat,
                                                       filename = logFileName)
        logfile = os.path.join(os.path.dirname(__file__), 'logfiles', filename)
        logging.basicConfig(filename=logfile, level=20)

    def new_entry(self, desc1, desc2, outcome, level=logLevelInfo):
        #
        log_msg = self._create_msg(desc1, desc2, outcome)
        #
        if level == logLevelCritical:
            level = 50
        elif level == logLevelError:
            level = 40
        elif level == logLevelWarning:
            level = 30
        else:
            level = 20
        self._log(log_msg, level)

    @staticmethod
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

    def _create_msg(self, desc1, desc2, outcome):
        #
        msg = ':{timestamp}::{desc1}::{desc2}::{outcome}'.format(timestamp=self._timestamp(),
                                                                 desc1=desc1,
                                                                 desc2=desc2,
                                                                 outcome=outcome)
        #
        return msg

    @staticmethod
    def _timestamp():
        return datetime.now().strftime(timeformat)
