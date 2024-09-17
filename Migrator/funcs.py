from lxml import etree
import json
import uuid
import re

import common

def get_timer_config(step, wk_dict):
    val = step.find('./activityConfig/properties/value')
    #print(f'timer config: timeInterval = {val.attrib["timeInterval"]}, intervalUnit = {val.attrib["intervalUnit"]}, runOnce = {val.attrib["runOnce"]}')
    time_interval = int(val.attrib["timeInterval"])
    time_unit = val.attrib["intervalUnit"]
    if time_unit == 'Second':
        time_unit = 'minutes'
        time_interval = int(time_interval / 60) if int(time_interval / 60) >=5 else 5
    wk_dict['code']['provider'] = 'clock'
    wk_dict['code']['name'] = 'scheduled_event'
    wk_dict['code']['input']['time_unit'] = time_unit
    wk_dict['code']['input']['trigger_every'] = str(time_interval)
    wk_dict['code']['uuid'] = str(uuid.uuid4())
    wk_conf_dict = json.loads(common.workato_conf_json)
    wk_conf_dict['provider'] = 'clock'
    wk_dict['config'].append(wk_conf_dict)


def get_log_expr(step, wk_dict, num):
    expr = step.xpath('./../../tibex:inputBindings/tibex:inputBinding', namespaces=common.ns)[0].attrib['expression']
    expr = expr.split('<message>')[1].split('</message>')[0]
    expr = convert_xslt_to_ruby(expr).removesuffix('&quot;').removeprefix('&quot;')
    if expr.startswith('$'):
        expr = get_data_pill('output', 'workato_variable', expr[1:])
    print(expr)
    wk_blk_dict = json.loads(common.workato_blk_json)
    wk_blk_dict['number'] = num
    wk_blk_dict['provider'] = 'logger'
    wk_blk_dict['name'] = 'log_message'
    wk_blk_dict['as'] = str(num)
    wk_blk_dict['input']['message'] = expr
    wk_blk_dict['uuid'] = str(uuid.uuid4())
    wk_dict['code']['block'].append(wk_blk_dict)
    wk_conf_dict = json.loads(common.workato_conf_json)
    wk_conf_dict['provider'] = 'logger'
    wk_dict['config'].append(wk_conf_dict)


def get_var_conf(tib_var, wk_dict, num):
    try:
        literal_elements = tib_var.xpath('./bpws:from/bpws:literal', namespaces=common.ns)
        if literal_elements and literal_elements[0].text:
            val = literal_elements[0].text.strip('"')
        else:
            val = ""
        
        print(f"Variable: {tib_var.get('name')}, Value: {val}")
        
        workato_var_schema_dict = json.loads(common.workato_var_schema_json)
        workato_var_schema_dict['name'] = tib_var.get('name')
        workato_var_schema_dict['label'] = tib_var.get('name')
        var_type = tib_var.get('type', '')
        workato_var_schema_dict['type'] = var_type.split(':')[-1] if ':' in var_type else var_type
        workato_var_schema_dict['details']['real_name'] = tib_var.get('name')
        
        workato_vars_json = json.loads(common.workato_vars_json)
        workato_vars_json['variables']['schema'] = '[' + json.dumps(workato_var_schema_dict) + ']'
        workato_vars_json['variables']['data'][tib_var.get('name')] = val
        
        wk_blk_dict = json.loads(common.workato_blk_json)
        wk_blk_dict['number'] = num
        wk_blk_dict['provider'] = 'workato_variable'
        wk_blk_dict['name'] = 'declare_variable'
        wk_blk_dict['as'] = str(num)
        wk_blk_dict['input'] = workato_vars_json
        wk_blk_dict['visible_config_fields'].append('variables.data.' + tib_var.get('name'))
        wk_blk_dict['uuid'] = str(uuid.uuid4())
        
        wk_dict['code']['block'].append(wk_blk_dict)
        wk_conf_dict = json.loads(common.workato_conf_json)
        wk_conf_dict['provider'] = 'workato_variable'
        wk_dict['config'].append(wk_conf_dict)
    except Exception as e:
        print(f"Error processing variable {tib_var.get('name')}: {str(e)}")
        # You might want to log this error or handle it in some way


def get_data_pill(pill_type, provider, expr):
    wk_data_pill_dict = json.loads(common.workato_data_pill_json)
    wk_data_pill_dict['pill_type'] = pill_type
    wk_data_pill_dict['provider'] = provider
    wk_data_pill_dict['line'] = '1'
    wk_data_pill_dict['path'].append(expr)
    return '#{_dp(\'' + json.dumps(wk_data_pill_dict) + '\')}'


def convert_xslt_to_ruby(xslt_code):
    # Convert XSLT templates to Ruby methods
    xslt_code = re.sub(r'<xsl:template match="(.*?)">', r'def template_\1', xslt_code)
    xslt_code = re.sub(r'</xsl:template>', r'end', xslt_code)

    # Convert xsl:value-of to Nokogiri's XPath selection
    #xslt_code = re.sub(r'<xsl:value-of select="(.*?)" ?/>', r'puts doc.xpath("\1").text', xslt_code)
    xslt_code = re.sub(r'<xsl:value-of select="(.*?)" ?/>', r'\1', xslt_code)

    # Convert xsl:for-each to Ruby each loop
    xslt_code = re.sub(r'<xsl:for-each select="(.*?)">', r'\1.each do |node|', xslt_code)
    xslt_code = re.sub(r'</xsl:for-each>', r'end', xslt_code)

    # Convert xsl:if to Ruby if statements
    xslt_code = re.sub(r'<xsl:if test="(.*?)">', r'if \1', xslt_code)
    xslt_code = re.sub(r'</xsl:if>', r'end', xslt_code)

    # Clean up any remaining XSLT tags
    xslt_code = re.sub(r'<xsl:(.*?)>', r'# \1', xslt_code)
    xslt_code = re.sub(r'</xsl:(.*?)>', r'# end \1', xslt_code)

    return xslt_code