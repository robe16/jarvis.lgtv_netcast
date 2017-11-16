serviceName = 'Jarvis: LGTV (Netcast OS)'
serviceType = 'lgtv_netcast'

logFileName = 'lgtv_netcast'
logFileNameTimeformat = '%Y-%m-%d'

logLevelUnset = 'unset'
logLevelDebug = 'debug'
logLevelInfo = 'info'
logLevelWarning = 'warning'
logLevelError = 'error'
logLevelCritical = 'critical'

logDescDevicePairing = 'Device pairing'
logDescDeviceShowpairkey = 'Show pairing key'
logDescDeviceGetapplist = 'Get app list'
logDescDeviceGetappicon = 'Get app icon'
logDescDeviceGetcurrentchannel = 'Get current channel'
logDescDeviceExecuteapp = 'Execute app'
logDescDeviceSendcommand = 'Send command'

logCategoryClient = 'client request'
logCategoryProcess = 'process'
logCategoryDevice = 'service'

timeformat = '%Y/%m/%d %H.%M.%S.%f'

uri_config = '/config'
uri_info = '/info/<resource_requested>'
uri_commands = '/commands'
uri_command = '/command'
uri_image = '/img/<filename>'

httpStatusSuccess = 200
httpStatusBadrequest = 400
httpStatusForbidden = 404
httpStatusFailure = 420
httpStatusServererror = 500

jarvis_broadcastFromPort = 4999
jarvis_broadcastPort = 5000
jarvis_broadcast_msg = 'jarvis::{service_id}::{service_type}::{port}'
