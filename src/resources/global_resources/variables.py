serviceName = 'Jarvis: LGTV (Netcast OS)'
serviceType = 'tv_lg_netcast'

logFileNameTimeformat = '%Y-%m-%d'

# NOTE: delimiter-separated value in log files is '::'
logMsg_Inbound_Info = ':{timestamp}::{serviceid}::{servicetype}::INBOUND::{result}::{ip}::{uri}::{method}::{httpresponse}::{desc}'
logMsg_Inbound_Error = ':{timestamp}::{serviceid}::{servicetype}::INBOUND::{result}::{exception}::{ip}::{uri}::{method}::{httpresponse}::{desc}'
logMsg_Internal_Info = ':{timestamp}::{serviceid}::{servicetype}::INTERNAL::{result}::{operation}::{desc}'
logMsg_Internal_Error = ':{timestamp}::{serviceid}::{servicetype}::INTERNAL::{result}::{exception}::{operation}::{desc}'
logMsg_Outbound_Info = ':{timestamp}::{serviceid}::{servicetype}::OUTBOUND::{result}::{ip}::{uri}::{method}::{httpresponse}::{desc}'
logMsg_Outbound_Error = ':{timestamp}::{serviceid}::{servicetype}::OUTBOUND::{result}::{exception}::{ip}::{uri}::{method}::{httpresponse}::{desc}'

logPass = 'PASS'
logFail = 'FAIL'
logException = 'EXCEPTION'

logDescDevicePairing = 'Device pairing'
logDescDeviceShowpairkey = 'Show pairing key'
logDescDeviceGetapplist = 'Get app list'
logDescDeviceGetappicon = 'Get app icon'
logDescDeviceGetcurrentchannel = 'Get current channel'
logDescDeviceExecuteapp = 'Execute app'
logDescDeviceSendcommand = 'Send command'

timeformat = '%Y/%m/%d %H.%M.%S.%f'

uri_config = '/config'
uri_commands = '/commands'
uri_command = '/command'
uri_apps_all = '/apps/all'
uri_apps_single = '/apps/single/<auid>'
uri_image_appicon = '/img/appicon/<auid>'
format_uri_image_appicon = '/img/appicon/{auid}'

httpStatusSuccess = 200
httpStatusBadrequest = 400
httpStatusForbidden = 404
httpStatusFailure = 420
httpStatusServererror = 500

jarvis_broadcastPort = 5000
jarvis_broadcast_msg = 'jarvis::discovery::{service_id}::{service_type}::{port}'
