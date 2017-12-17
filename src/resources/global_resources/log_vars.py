# NOTE: delimiter-separated value in log files is '::'
logMsg_Inbound_Info = ':{timestamp}::{serviceid}::{servicetype}::INBOUND::{result}::{client}::{uri}::{method}::{httpresponse}::{desc}'
logMsg_Inbound_Error = ':{timestamp}::{serviceid}::{servicetype}::INBOUND::{result}::{exception}::{client}::{uri}::{method}::{httpresponse}::{desc}'
logMsg_Internal_Info = ':{timestamp}::{serviceid}::{servicetype}::INTERNAL::{result}::{operation}::{desc}'
logMsg_Internal_Error = ':{timestamp}::{serviceid}::{servicetype}::INTERNAL::{result}::{exception}::{operation}::{desc}'
logMsg_Outbound_Info = ':{timestamp}::{serviceid}::{servicetype}::OUTBOUND::{result}::{ip}::{uri}::{method}::{httpresponse}::{desc}'
logMsg_Outbound_Error = ':{timestamp}::{serviceid}::{servicetype}::OUTBOUND::{result}::{exception}::{ip}::{uri}::{method}::{httpresponse}::{desc}'

logPass = 'PASS'
logFail = 'FAIL'
logException = 'EXCEPTION'

logFileNameTimeformat = '%Y-%m-%d'
logTimeformat = '%Y/%m/%d %H.%M.%S.%f'
