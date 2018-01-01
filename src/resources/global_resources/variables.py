serviceName = 'Jarvis: LGTV (Netcast OS)'
serviceType = 'tv_lg_netcast'

uri_config = '/config'
uri_commands = '/commands'
uri_command_keyInput = '/command/keyInput'
uri_command_executeApp = '/command/executeApp'
uri_command_cursorVisbility = '/command/cursor/visibility'
uri_command_touchMove = '/command/touch/move'
uri_command_touchClick = '/command/touch/click'
uri_command_touchWheel = '/command/touch/wheel'
uri_volume = '/volume'
uri_apps_all = '/apps/all'
uri_apps_single = '/apps/single/<auid>'
uri_image_appicon = '/img/appicon/<auid>'
uri_image_screenshot = '/img/screenshot'
uri_3d = '/3d'

format_uri_image_appicon = '/img/appicon/{auid}'

service_header_clientid_label = 'jarvis.client-service'

httpStatusSuccess = 200
httpStatusBadrequest = 400
httpStatusForbidden = 404
httpStatusFailure = 420
httpStatusServererror = 500

jarvis_broadcastPort = 5000
jarvis_broadcast_msg = 'jarvis::discovery::{service_id}::{service_type}::{port}'
