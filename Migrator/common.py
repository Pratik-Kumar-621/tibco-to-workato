ns = {'bpws': 'http://docs.oasis-open.org/wsbpel/2.0/process/executable',
      'bwext': 'http://tns.tibco.com/bw/model/core/bwext',
      'tibex': 'http://www.tibco.com/bpel/2007/extensions',
      'sca-bpel': 'http://docs.oasis-open.org/ns/opencsa/sca-bpel/200801'}


workato_json = '''
{
    "name": "",
    "version": 1,
    "private": true,
    "concurrency": 1,
    "code": {
        "number": 0,
        "provider": "",
        "name": "",
        "as": "0",
        "keyword": "trigger",
        "input": {
        },
        "block": [
        ],
        "uuid": "",
        "unfinished": false 
    },
    "config": [
    ]
}
'''

workato_blk_json = '''
{
    "number": 1,
    "provider": "",
    "name": "",
    "as": "1",
    "keyword": "action",
    "input": {
    },
    "visible_config_fields": [
    ],
    "uuid": ""
}
'''

workato_conf_json = '''
{
    "keyword": "application",
    "provider": "",
    "skip_validation": false
}
'''

workato_var_schema_json = '''
{
    "name": "",
    "type": "",
    "optional": true,
    "label": "",
    "details": {
        "real_name": ""
    },
    "control_type": "text"
}
'''

workato_vars_json = '''
{
    "variables": {
        "schema": "",
        "data": {} 
    }
}
'''

workato_data_pill_json = '''
{
    "pill_type": "",
    "provider": "",
    "line": "",
    "path": [
    ]
}
'''