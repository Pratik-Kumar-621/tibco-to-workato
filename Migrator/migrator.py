#from saxonche import PySaxonProcessor
from lxml import etree
import json
import uuid
import zipfile

import common
import funcs

wk_dict = json.loads(common.workato_json)
el = etree.parse('./in/ProcessWithInput.bwp')
#print(etree.tostring(el))
proc = el.getroot()
#print(proc.tag)

recipe = proc.attrib['name'].split('.')[1].replace(' ', '_')
print(f'recipe = {recipe}')
wk_dict['name'] = recipe

num = 1
tib_vars = proc.xpath('.//bpws:variable[not(@sca-bpel:internal="true" or @sca-bpel:privateProperty="true")]', namespaces=common.ns)
for tib_var in tib_vars:
    funcs.get_var_conf(tib_var, wk_dict, num)
    num += 1

flows = proc.xpath('.//bpws:flow', namespaces=common.ns)
#print(flows)
activities = flows[0].xpath('.//bwext:BWActivity', namespaces=common.ns)
#print(activities)

for activity in activities:
    activity_type = activity.attrib['activityTypeID']
    print(activity_type)
    if activity_type == 'bw.generalactivities.timer':
        funcs.get_timer_config(activity, wk_dict)
        num -= 1    
    elif activity_type == 'bw.generalactivities.log':
        funcs.get_log_expr(activity, wk_dict, num)
    num += 1

#print(json.dumps(wk_dict, indent=4))
out_filepath = './out/' + recipe + '.recipe.json'
with open(out_filepath, 'w') as fout:
    fout.write(json.dumps(wk_dict, indent=4))

zip = zipfile.ZipFile('./out/migrated.zip', 'w', zipfile.ZIP_DEFLATED)
zip.write(out_filepath)
zip.close()
