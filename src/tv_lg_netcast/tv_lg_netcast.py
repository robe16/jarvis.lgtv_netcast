import datetime
import xml.etree.ElementTree as ET
import requests as requests
from multiprocessing import Manager, Process

from resources.global_resources.variables import *
from parameters import app_check_period
from log.log import log_outbound
from config.config import get_cfg_details_ip, get_cfg_details_pairingkey

# Issue with IDE and production running of script - resolved with try/except below
try:
    # IDE
    from tv_lg_netcast.commands import commands
except:
    # Production
    from commands import commands

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class TvLgNetcast():

    lgtv_session = requests.Session()

    STRtv_PATHpair = '/udap/api/pairing'
    STRtv_PATHcommand = '/udap/api/command'
    STRtv_PATHevent = '/udap/api/event'
    STRtv_PATHquery = '/udap/api/data'

    apps_list_dict = Manager().dict()
    apps_img_dict = Manager().dict()

    def __init__(self):
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
            log_outbound(r_pass, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), uri, 'POST', r.status_code)
            #
            return r_pass
            #
        except requests.exceptions.ConnectionError as e:
            log_outbound(False, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), uri, 'POST', '-', exception='connection error: {e}'.format(e=e))
            return False
            #
        except Exception as e:
            log_outbound(False, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), uri, 'POST', '-', exception=e)
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
            log_outbound(r_pass, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), uri, 'POST', r.status_code)
            #
            return r_pass
            #
        except Exception as e:
            log_outbound(False, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), uri, 'POST', '-', exception=e)
            return False

    def _app_check(self, attempt=1):
        #
        if len(self.apps_list_dict) == 0 or self.apps_timestamp > (datetime.datetime.now() + datetime.timedelta(minutes=app_check_period)):
            self._get_apps()
        #
        if len(self.apps_list_dict) > 0:
            return
        elif len(self.apps_list_dict) == 0 and attempt < 3:
            attempt += 1
            self._app_check(attempt)
        else:
            raise Exception

    def _get_apps(self):
        self.apps_timestamp = datetime.datetime.now()
        self.apps_list_dict = self._getApplist()

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
            r_pass = (r.status_code == requests.codes.ok)
            #
            log_outbound(r_pass, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), uri, 'GET', r.status_code)
            #
            if not r_pass:
                self.is_paired = False
                if not self._check_paired(pair_reason=desc1):
                    return False
                r = self.lgtv_session.get(url, timeout=2)
                r_pass = (r.status_code == requests.codes.ok)
                log_outbound(r_pass, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), uri, 'GET', r.status_code)
            #
            if r_pass:
                #
                xml = ET.fromstring(r.content)
                dict_apps = {}
                #
                for data in xml[0]:
                    try:
                        temp_dict = {}
                        temp_dict['auid'] = data.find('auid').text
                        temp_dict['name'] = data.find('name').text
                        temp_dict['type'] = data.find('type').text
                        temp_dict['cpid'] = data.find('cpid').text
                        temp_dict['adult'] = data.find('adult').text
                        temp_dict['icon_name'] = data.find('icon_name').text
                        dict_apps[data.find('auid').text] = temp_dict
                        #
                        self.apps_img_dict[data.find('auid').text] = self._getAppicon(data.find('auid').text,
                                                                                      data.find('name').text.replace(' ','%20'))
                    except:
                        pass
                return dict_apps
            else:
                return False
        except Exception as e:
            log_outbound(False, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), self.STRtv_PATHquery,
                         'GET', '-', exception=e)
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
        #
        r_pass = (r.status_code == requests.codes.ok)
        #
        log_outbound(r_pass, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), uri, 'GET', r.status_code)
        #
        if not r_pass:
            self.is_paired = False
            if not self._check_paired(pair_reason=desc1):
                return False
            r = self.lgtv_session.get(url, timeout=2)
            r_pass = (r.status_code == requests.codes.ok)
            log_outbound(r_pass, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), uri, 'GET', r.status_code)
        #
        if r_pass:
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
        # #
        # r_pass = (r.status_code == requests.codes.ok)
        # #
        # log_outbound(r_pass, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), uri, 'GET', r.status_code)
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

    def getApps_all(self):
        try:
            self._app_check()
            return self.apps_list_dict
        except Exception as e:
            return False

    def getApps_single(self, auid):
        try:
            self._app_check()
            return self.apps_list_dict[auid]
        except Exception as e:
            return False

    def getImage_app(self, auid):
        try:
            self._app_check()
            return self.apps_img_dict[auid]
        except Exception as e:
            return False

    def executeApp(self, auid):
        #
        name = self.apps_list_dict[auid]['name']
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
            log_outbound(False, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), self.STRtv_PATHcommand, 'POST', '-', exception=e)
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
            log_outbound(False, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), self.STRtv_PATHcommand, 'POST', '-', exception=e)
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
        #
        r_pass = (r.status_code == requests.codes.ok)
        #
        log_outbound(r_pass, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), uri, 'POST', r.status_code)
        #
        if not r.status_code == requests.codes.ok:
            self.is_paired = False
            if not self._check_paired(pair_reason=desc1):
                return False
            r = self.lgtv_session.post(url, STRxml, timeout=2)
            r_pass = (r.status_code == requests.codes.ok)
            log_outbound(r_pass, '{ip}:{port}'.format(ip=self._ipaddress, port=self._port), uri, 'POST', r.status_code)
        #
        return r_pass
