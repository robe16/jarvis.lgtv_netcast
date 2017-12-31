import datetime
import xml.etree.ElementTree as ET
import requests as requests
from multiprocessing import Manager, Process

from common_functions.urlencode import url_encode
from resources.lang.enGB.logs import *
from resources.global_resources.log_vars import logPass, logFail, logException
from parameters import app_check_period
from log.log import log_outbound
from config.config import get_cfg_details_ip, get_cfg_details_pairingkey
from commands import commands

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# For reference:
# http://developer.lgappstv.com/TV_HELP/index.jsp?topic=%2Flge.tvsdk.references.book%2Fhtml%2FUDAP%2FUDAP%2FLG+UDAP+2+0+Service+Profiles.htm

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
        if not pair_reason == '':
            pair_reason = '{action} - {pair_reason}'.format(action=logDescDevicePairing,
                                                            pair_reason=pair_reason)
        else:
            pair_reason = logDescDevicePairing
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
            result = logPass if r_pass else logFail
            #
            log_outbound(result,
                         self._ipaddress, self._port, 'POST', uri,
                         '-', '-',
                         r.status_code,
                         description=pair_reason)
            #
            return r_pass
            #
        except requests.exceptions.ConnectionError as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'POST', uri,
                         '-', '-',
                         '-',
                         description=pair_reason,
                         exception='connection error: {e}'.format(e=e))
            return False
            #
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'POST', uri,
                         '-', '-',
                         '-',
                         description=pair_reason,
                         exception=e)
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
            result = logPass if r_pass else logFail
            #
            log_outbound(result,
                         self._ipaddress, self._port, 'POST', uri,
                         '-', '-',
                         r.status_code,
                         description=logDescDeviceShowpairkey)
            #
            return r_pass
            #
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'POST', uri,
                         '-', '-',
                         '-',
                         description=logDescDeviceShowpairkey,
                         exception=e)
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
        try:
            #
            if not self._check_paired(pair_reason=logDescDeviceGetapplist):
                return False
            #
            uri = self.STRtv_PATHquery
            #
            query = 'target=applist_get'
            query += '&type={type}'.format(type=str(APPtype))
            query += '&index={index}'.format(index=str(APPindex))
            query += '&number={number}'.format(number=str(APPnumber))
            #
            url = 'http://{ipaddress}:{port}{uri}?{query}'.format(ipaddress=self._ipaddress,
                                                                  port=str(self._port),
                                                                  uri=uri,
                                                                  query=query)
            #
            r = self.lgtv_session.get(url, timeout=2)
            #
            r_pass = (r.status_code == requests.codes.ok)
            #
            result = logPass if r_pass else logFail
            #
            log_outbound(result,
                         self._ipaddress, self._port, 'GET', uri, query, '-',
                         r.status_code,
                         description=logDescDeviceGetapplist)
            #
            if not r_pass:
                self.is_paired = False
                if not self._check_paired(pair_reason=logDescDeviceGetapplist):
                    return False
                r = self.lgtv_session.get(url, timeout=2)
                r_pass = (r.status_code == requests.codes.ok)
                #
                result = logPass if r_pass else logFail
                #
                log_outbound(result,
                             self._ipaddress, self._port, 'GET', uri, query, '-',
                             r.status_code,
                             description=logDescDeviceGetapplist)
            #
            if r_pass:
                #
                xml = ET.fromstring(r.content)
                dict_apps = {}
                #
                for data in xml.find('dataList'):
                    try:
                        dict_apps[data.find('auid').text] = {'auid': data.find('auid').text,
                                                             'name': data.find('name').text,
                                                             'type': data.find('type').text,
                                                             'cpid': data.find('cpid').text,
                                                             'adult': data.find('adult').text,
                                                             'icon_name': data.find('icon_name').text}
                        #
                        self.apps_img_dict[data.find('auid').text] = self._getAppicon(data.find('auid').text,
                                                                                      url_encode(data.find('name').text))
                    except:
                        pass
                return dict_apps
            else:
                return False
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'GET', self.STRtv_PATHquery,
                         '-', '-',
                         '-',
                         description=logDescDeviceGetapplist,
                         exception=e)
            return False

    def _getAppicon(self, auid, name):
        #
        try:
            #
            query = 'target=appicon_get'
            query += '&auid={auid}'.format(auid=auid)
            query += '&appname={appname}'.format(appname=name)
            #
            return self._send_query(query, logDescDeviceGetappicon)
            #
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'GET', self.STRtv_PATHquery,
                         '-', '-',
                         '-',
                         description=logDescDeviceGetappicon,
                         exception=e)
            return False

    # def _getChannel_current(self):
    #     #
    #     # TODO - TEST!!
    #     #
    #     uri = self.STRtv_PATHquery + '?target=cur_channel'
    #     #
    #     url = 'http://{ipaddress}:{port}{uri}'.format(ipaddress=self._ipaddress, port=str(self._port), uri=uri)
    #     #
    #     r = self.lgtv_session.get(url, timeout=2)
    #     #
    #     r_pass = (r.status_code == requests.codes.ok)
    #     #
    #     result = logPass if r_pass else logFail
    #     #
    #     log_outbound(result,
    #                  self._ipaddress, self._port, 'GET', uri,
    #                  '-', '-',
    #                  r.status_code,
    #                  description=logDescDeviceGetcurrentchannel)
    #     #
    #     if not r_pass:
    #         self.is_paired = False
    #         if not self._check_paired(pair_reason=logDescDeviceGetcurrentchannel):
    #             return False
    #         r = self.lgtv_session.get(url, timeout=2)
    #         r_pass = (r.status_code == requests.codes.ok)
    #         #
    #         result = logPass if r_pass else logFail
    #         #
    #         log_outbound(result,
    #                      self._ipaddress, self._port, 'GET', uri,
    #                      '-', '-',
    #                      r.status_code,
    #                      description=logDescDeviceGetcurrentchannel)
    #     #
    #     if r_pass:
    #         #
    #         xml = ET.fromstring(r.content)
    #         data = xml.find('dataList').find('data')
    #         #
    #         return {'name': data.find('chname').text}
    #     else:
    #         return False
    #
    # def getChannel_current(self):
    #     return self._getChannel_current()

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
        STRxml = '<?xml version="1.0" encoding="utf-8"?>'
        STRxml += '<envelope><api type="command">'
        STRxml += '<name>AppExecute</name>'
        STRxml += '<auid>{auid}</auid>'.format(auid=auid)
        STRxml += '<appname>{app_name}</appname>'.format(app_name=name.replace(' ','%20'))
        #STRxml += '<contentId>Content ID</contentId>'
        STRxml += '</api></envelope>'
        #
        try:
            return self._send_command(STRxml, logDescDeviceExecuteapp)
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'POST', self.STRtv_PATHcommand,
                         '-', '-',
                         '-',
                         description=logDescDeviceGetapplist,
                         exception=e)
            return False

    def sendCmd(self, key):
        #
        STRxml = '<?xml version="1.0" encoding="utf-8"?>'
        STRxml += '<envelope><api type="command">'
        STRxml += '<name>HandleKeyInput</name>'
        STRxml += '<value>{value}</value>'.format(value=commands[key])
        STRxml += '</api></envelope>'
        #
        try:
            return self._send_command(STRxml, logDescDeviceSendcommand)
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'POST', self.STRtv_PATHcommand,
                         '-', '-',
                         '-',
                         description=logDescDeviceSendcommand,
                         exception=e)
            return False

    def getVolume(self):
        #
        try:
            #
            query = 'target=volume_info'
            #
            r = self._send_query(query, logDescDeviceGetvolume)
            #
            if bool(r):
                #
                # <?xml version="1.0" encoding="utf-8"?>
                # <envelope>
                #   <dataList name="Volume Info">
                #     <data>
                #       <mute>true or false</mute>
                #       <minLevel>Minimum volume level</minLevel>
                #       <maxLevel>Maximum volume level</maxLevel>
                #       <level>Current volume level</level>
                #     </data>
                #   </dataList>
                # </envelope>
                #
                data = ET.fromstring(r.content).find('dataList').find('data')
                #
                return {'mute': data.find('mute').text == 'true',
                        'minLevel': data.find('minLevel').text,
                        'maxLevel': data.find('maxLevel').text,
                        'level': data.find('level').text}
            else:
                return False
            #
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'GET', self.STRtv_PATHquery,
                         '-', '-',
                         '-',
                         description=logDescDeviceGetvolume,
                         exception=e)
            return False

    def get3d(self):
        #
        try:
            #
            query = 'target=is_3d'
            #
            r = self._send_query(query, logDescDeviceGet3d)
            #
            if bool(r):
                #
                # <?xml version="1.0" encoding="utf-8"?>
                # <envelope>
                #   <dataList name="is3D">
                #     <data>
                #       <is3D>true or false</is3D>
                #     </data>
                #   </dataList>
                # </envelope>
                #
                data = ET.fromstring(r.content).find('dataList').find('data')
                #
                return {'is3D': data.find('is3D').text == 'true'}
            else:
                return False
            #
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'GET', self.STRtv_PATHquery,
                         '-', '-',
                         '-',
                         description=logDescDeviceGet3d,
                         exception=e)
            return False

    def getImage_screenshot(self):
        #
        try:
            #
            query = 'target=screen_image'
            #
            return self._send_query(query, logDescDeviceGetscreenshot)
            #
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'GET', self.STRtv_PATHquery,
                         '-', '-',
                         '-',
                         description=logDescDeviceGetscreenshot,
                         exception=e)
            return False

    def sendChannel(self, major, minor, sourceIndex, physicalNum):
        #
        STRxml = '<?xml version="1.0" encoding="utf-8"?>'
        STRxml += '<envelope><api type="command">'
        STRxml += '<name>HandleChannelChange</name>'
        STRxml += '<major>{major}</major>'.format(major=major)
        STRxml += '<minor>{minor}</minor>'.format(minor=minor)
        STRxml += '<sourceIndex>{sourceIndex}</sourceIndex>'.format(sourceIndex=sourceIndex)
        STRxml += '<physicalNum>{physicalNum}</physicalNum>'.format(physicalNum=physicalNum)
        STRxml += '</api></envelope>'
        #
        try:
            return self._send_command(STRxml, logDescDeviceSendchannel)
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'POST', self.STRtv_PATHcommand,
                         '-', '-',
                         '-',
                         description=logDescDeviceSendchannel,
                         exception=e)
            return False

    def sendTouchmove(self, x, y):
        #
        STRxml = '<?xml version="1.0" encoding="utf-8"?>'
        STRxml += '<envelope><api type="command">'
        STRxml += '<name>HandleTouchMove</name>'
        STRxml += '<x>{x}</x>'.format(x=x)
        STRxml += '<y>{y}</y>'.format(y=y)
        STRxml += '</api></envelope>'
        #
        try:
            return self._send_command(STRxml, logDescDeviceTouchmove)
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'POST', self.STRtv_PATHcommand,
                         '-', '-',
                         '-',
                         description=logDescDeviceTouchmove,
                         exception=e)
            return False

    def sendTouchclick(self):
        #
        STRxml = '<?xml version="1.0" encoding="utf-8"?>'
        STRxml += '<envelope><api type="command">'
        STRxml += '<name>HandleTouchClick</name>'
        STRxml += '</api></envelope>'
        #
        try:
            return self._send_command(STRxml, logDescDeviceTouchclick)
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'POST', self.STRtv_PATHcommand,
                         '-', '-',
                         '-',
                         description=logDescDeviceTouchclick,
                         exception=e)
            return False

    def sendTouchwheel(self, direction):
        #
        STRxml = '<?xml version="1.0" encoding="utf-8"?>'
        STRxml += '<envelope><api type="command">'
        STRxml += '<name>HandleTouchWheel</name>'
        STRxml += '<value>{direction}</value>'.format(direction=direction)
        STRxml += '</api></envelope>'
        #
        try:
            return self._send_command(STRxml, logDescDeviceTouchwheel)
        except Exception as e:
            #
            log_outbound(logException,
                         self._ipaddress, self._port, 'POST', self.STRtv_PATHcommand,
                         '-', '-',
                         '-',
                         description=logDescDeviceTouchwheel,
                         exception=e)
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
        result = logPass if r_pass else logFail
        #
        log_outbound(result,
                     self._ipaddress, self._port, 'POST', uri,
                     '-', '-',
                     r.status_code)
        #
        if not r.status_code == requests.codes.ok:
            self.is_paired = False
            if not self._check_paired(pair_reason=desc1):
                return False
            r = self.lgtv_session.post(url, STRxml, timeout=2)
            r_pass = (r.status_code == requests.codes.ok)
            #
            result = logPass if r_pass else logFail
            #
            log_outbound(result,
                         self._ipaddress, self._port, 'POST', uri,
                         '-', '-',
                         r.status_code)
        #
        return r_pass

    def _send_query(self, query, desc1):
        #
        if not self._check_paired(pair_reason=desc1):
            return False
        #
        uri = self.STRtv_PATHquery
        #
        url = 'http://{ipaddress}:{port}{uri}?{query}'.format(ipaddress=self._ipaddress,
                                                              port=str(self._port),
                                                              uri=uri,
                                                              query=query)
        #
        r = self.lgtv_session.get(url, timeout=2)
        #
        r_pass = (r.status_code == requests.codes.ok)
        #
        result = logPass if r_pass else logFail
        #
        log_outbound(result,
                     self._ipaddress, self._port, 'GET', uri, query, '-',
                     r.status_code)
        #
        if not r.status_code == requests.codes.ok:
            self.is_paired = False
            if not self._check_paired(pair_reason=desc1):
                return False
            r = self.lgtv_session.get(url, timeout=2)
            r_pass = (r.status_code == requests.codes.ok)
            #
            result = logPass if r_pass else logFail
            #
            log_outbound(result,
                         self._ipaddress, self._port, 'GET', uri, query, '-',
                         r.status_code)
        #
        if r_pass:
            return r.content
        else:
            return False
