import datetime
import xml.etree.ElementTree as ET
import requests as requests
from multiprocessing import Manager, Process

from resources.global_resources.variables import *
from parameters import app_check_period
from log.log import Log
from config.config import get_cfg_details_ip, get_cfg_details_pairingkey

# Issue with IDE and production running of script - resolved with try/except below
try:
    # IDE
    from lgtv_netcast.commands import commands
except:
    # Production
    from commands import commands

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class tv_lg_netcast():

    lgtv_session = requests.Session()

    STRtv_PATHpair = '/udap/api/pairing'
    STRtv_PATHcommand = '/udap/api/command'
    STRtv_PATHevent = '/udap/api/event'
    STRtv_PATHquery = '/udap/api/data'

    apps_dict = Manager().dict()

    def __init__(self):
        #
        self._log = Log()
        #
        self._ipaddress = get_cfg_details_ip()
        self._port = 8080
        self._pairingkey = get_cfg_details_pairingkey()
        #
        self.is_paired = False
        self.apps_timestamp = False
        #
        self.create_session()
        #
        Process(target=self._start_instance).start()

    def _start_instance(self):
        if self._pair_device():
            self._get_apps()

    def create_session(self):
        with requests.Session() as s:
            s.headers.update({'User-Agent': 'Linux/2.6.18 UDAP/2.0 CentOS/5.8',
                              'content-type': 'text/xml; charset=utf-8'})
        self.lgtv_session = s

    def _pair_device(self, pair_reason=''):
        #
        desc1 = logDescDevicePairing
        #
        if not pair_reason=='':
            desc1 += ' - {pair_reason}'.format(pair_reason=pair_reason)
        #
        STRxml = '<?xml version="1.0" encoding="utf-8"?><envelope><api type="pairing"><name>hello</name>'
        STRxml += '<value>{pairingkey}</value>'.format(pairingkey = self._pairingkey)
        STRxml += '<port>{port}</port>'.format(port=str(self._port))
        STRxml += '</api></envelope>'
        #
        uri = self.STRtv_PATHpair
        #
        url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress,
                                                      port=str(self._port),
                                                      uri=uri)
        #
        try:
            r = self.lgtv_session.post(url, STRxml, timeout=2)
            #
            r_pass = True if r.status_code == requests.codes.ok else False
            self.is_paired = r_pass
            #
            self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, r.status_code, level=self._get_log_level(r))
            #
            return r_pass
            #
        except requests.exceptions.ConnectionError as e:
            #
            self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, 'connection error: {e}'.format(e=e), level=logLevelWarning)
            #
            return False
            #
        except Exception as e:
            #
            self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, e, level=logLevelWarning)
            #
            return False

    def _check_paired(self, pair_reason=''):
        if not self.is_paired:
            count = 0
            while count < 2:
                self._pair_device(pair_reason)
                if self.is_paired:
                    return True
                count += 1
            if count == 5 and not self.is_paired:
                return False
        return True

    def show_pairingkey(self):
        #
        desc1 = logDescDeviceShowpairkey
        #
        STRxml = '<?xml version="1.0" encoding="utf-8"?><envelope><api type="pairing"><name>showKey</name></api></envelope>'
        #
        uri = self.STRtv_PATHpair
        #
        url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress,
                                                      port=str(self._port),
                                                      uri=uri)
        #
        try:
            r = self.lgtv_session.post(url, STRxml, timeout=2)
            r_pass = True if r.status_code == requests.codes.ok else False
            #
            self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, r.status_code, level=self._get_log_level(r))
            #
            return r_pass
            #
        except Exception as e:
            self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, e, level=logLevelError)
            return False

    def _app_check(self, attempt=1):
        #
        if len(self.apps_dict) == 0 or self.apps_timestamp > (datetime.datetime.now() + datetime.timedelta(minutes=app_check_period)):
            self._get_apps()
        #
        if len(self.apps_dict) > 0:
            return
        elif len(self.apps_dict) == 0 and attempt < 3:
            attempt += 1
            self._app_check(attempt)
        else:
            raise Exception

    def _get_apps(self):
        self.apps_timestamp = datetime.datetime.now()
        self.apps_dict = self._getApplist()

    def _getApplist(self, APPtype=3, APPindex=0, APPnumber=0):
        #
        desc1 = logDescDeviceGetapplist
        #
        try:
            #
            if not self._check_paired(pair_reason='getApplist'):
                return False
            #
            uri = '/udap/api/data?target=applist_get'
            uri += '&type={type}'.format(type=str(APPtype))
            uri += '&index={index}'.format(index=str(APPindex))
            uri += '&number={number}'.format(number=str(APPnumber))
            #
            url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress, port=str(self._port), uri=uri)
            #
            r = self.lgtv_session.get(url, timeout=2)
            #
            self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, r.status_code, level=self._get_log_level(r))
            #
            if not r.status_code == requests.codes.ok:
                self.is_paired = False
                if not self._check_paired(pair_reason=desc1):
                    return False
                r = self.lgtv_session.post(url, timeout=2)
                self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, r.status_code, level=self._get_log_level(r))
            #
            if r.status_code == requests.codes.ok:
                #
                xml = ET.fromstring(r.content)
                json_apps = {}
                #
                for data in xml[0]:
                    try:
                        json_a = {}
                        json_a['auid'] = data.find('auid').text
                        json_a['name'] = data.find('name').text
                        json_a['type'] = data.find('type').text
                        json_a['cpid'] = data.find('cpid').text
                        json_a['adult'] = data.find('adult').text
                        json_a['icon_name'] = data.find('icon_name').text
                        json_apps[data.find('auid').text] = json_a
                    except:
                        pass
                return json_apps
            else:
                return False
        except:
            return False

    def _getAppicon(self, auid, name):
        #
        desc1 = logDescDeviceGetappicon
        #
        if not self._check_paired(pair_reason=desc1):
            return False
        #
        # auid = This is the unique ID of the app, expressed as an 8-byte-long hexadecimal string.
        # name = App name
        uri = '/udap/api/data?target=appicon_get'
        uri += '&auid={auid}'.format(auid=auid)
        uri += '&appname={appname}'.format(appname=name)
        #
        url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress, port=str(self._port), uri=uri)
        #
        r = self.lgtv_session.get(url, timeout=2)
        self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, r.status_code, level=self._get_log_level(r))
        #
        if not r.status_code == requests.codes.ok:
            self.is_paired = False
            if not self._check_paired(pair_reason=desc1):
                return False
            r = self.lgtv_session.post(url, timeout=2)
            self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, r.status_code, level=self._get_log_level(r))
        #
        if r.status_code == requests.codes.ok:
            return r.content
        else:
            return False

    def getChan(self):
        #
        # TODO
        # desc1 = logDescDeviceGetcurrentchannel
        # #
        # uri = self.STRtv_PATHquery + '?target=cur_channel'
        # #
        # url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress, port=str(self._port), uri=uri)
        # #
        # r = self.lgtv_session.get(url, timeout=2)
        # self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, r.status_code, level=self._get_log_level(r))
        #
        return False

    def getCommands(self):
        #
        cmds = []
        #
        for c in commands['commands']:
            cmds.append(c)
        #
        return {'commands': cmds}

    def getInfo(self, resource_requested):
        try:
            if resource_requested == 'applist':
                self._app_check()
                return self.apps_dict
        except Exception as e:
            return False

    def getImage(self, auid, name):
        try:
            return self._getAppicon(auid, name.replace(' ','%20'))
        except Exception as e:
            return False

    def executeApp(self, auid, name):
        #
        desc1 = logDescDeviceExecuteapp
        #
        STRxml = '<?xml version="1.0" encoding="utf-8"?>'
        STRxml += '<envelope><api type="command">'
        STRxml += '<name>AppExecute</name>'
        STRxml += '<auid>{auid}</auid>'.format(auid=auid)
        STRxml += '<appname>{app_name}</appname>'.format(app_name=name.replace(' ','%20'))
        #STRxml += '<contentId>Content ID</contentId>'
        STRxml += '</api></envelope>'
        #
        try:
            return self._send_command(STRxml, desc1)
        except Exception as e:
            self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, '{auid} - {name}'.format(auid=auid, name=name), e, level=logLevelError)
            return False

    def sendCmd(self, key):
        #
        desc1 = logDescDeviceSendcommand
        #
        STRxml = '<?xml version="1.0" encoding="utf-8"?>'
        STRxml += '<envelope><api type="command">'
        STRxml += '<name>HandleKeyInput</name>'
        STRxml += '<value>{value}</value>'.format(value=commands[key])
        STRxml += '</api></envelope>'
        #
        try:
            return self._send_command(STRxml, desc1)
        except Exception as e:
            self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, commands[key], e, level=logLevelError)
            return False

    def _send_command(self, STRxml, desc1):
        #
        if not self._check_paired(pair_reason=desc1):
            return False
        #
        uri = self.STRtv_PATHcommand
        #
        url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress,
                                                      port=str(self._port),
                                                      uri=uri)
        #
        r = self.lgtv_session.post(url, STRxml, timeout=2)
        self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, r.status_code, level=self._get_log_level(r))
        #
        if not r.status_code == requests.codes.ok:
            self.is_paired = False
            if not self._check_paired(pair_reason=desc1):
                return False
            r = self.lgtv_session.post(url, STRxml, timeout=2)
            self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, r.status_code, level=self._get_log_level(r))
        #
        response = (r.status_code == requests.codes.ok)
        self._log.new_entry(logCategoryDevice, self._ipaddress, desc1, uri, r.status_code, level=self._get_log_level(r))
        #
        return response

    @staticmethod
    def _get_log_level(r):
        if r.status_code == requests.codes.ok:
            return logLevelWarning
        else:
            return logLevelInfo
