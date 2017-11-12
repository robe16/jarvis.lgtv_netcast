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
# LEVEL:user::%Y/%m/%d %H.%M.%S.%f::category::clientip/serverip/-::description-1::description-2::outcome

# NOTE: delimiter-separated value - '::'

class Log():

    def __init__(self):
        self._set_logfile()
        schedule.every().day.at("00:00").do(self._set_logfile)

    def _set_logfile(self):
        filename = '{timestamp} {filename}.log'.format(timestamp = datetime.now().strftime(logFileNameTimeformat),
                                                       filename = logFileName)
        logfile = os.path.join(os.path.dirname(__file__), 'logfiles', filename)
        logging.basicConfig(filename=logfile, level=20)

    def new_entry(self, category, ip, desc1, desc2, outcome, level=logLevelInfo):
        #
        log_msg = self._create_msg(category, ip, desc1, desc2, outcome)
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

    def _create_msg(self, category, ip, desc1, desc2, outcome):
        #
        msg = ':{timestamp}::{category}::{ip}::{desc1}::{desc2}::{outcome}'.format(timestamp=self._timestamp(),
                                                                                   category=category,
                                                                                   ip=ip,
                                                                                   desc1=desc1,
                                                                                   desc2=desc2,
                                                                                   outcome=outcome)
        #
        return msg

    @staticmethod
    def _timestamp():
        return datetime.now().strftime(timeformat)
