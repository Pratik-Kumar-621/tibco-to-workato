#from saxonche import PySaxonProcessor
from lxml import etree
import json
import uuid
import zipfile
import os
import common
import funcs

wk_dict = json.loads(common.workato_json)
# print(wk_dict)

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the bwp_files folder
bwp_folder = os.path.join(current_dir, 'bwp_files')

# Get the list of .bwp files in the folder
bwp_files = [f for f in os.listdir(bwp_folder) if f.endswith('.bwp')]

# Sort the files to ensure a000-HelloWorld.bwp comes first if it exists
bwp_files.sort()

if not bwp_files:
    print("Error: No .bwp files found in the bwp_files folder.")
    exit(1)

# Use the first .bwp file (which should be a000-HelloWorld.bwp if it exists)
input_file = os.path.join(bwp_folder, bwp_files[3])
print(f"Using input file: {input_file}")

# Get the base name of the input file (without extension)
base_name = os.path.splitext(os.path.basename(input_file))[0]

el = etree.parse(input_file)
proc = el.getroot()
print("root :"+proc.tag)

recipe = proc.attrib['name'].split('.')[1].replace(' ', '_')
# print(f'recipe = {recipe}')
wk_dict['name'] = recipe

num = 1
tib_vars = proc.xpath('.//bpws:variable[not(@sca-bpel:internal="true" or @sca-bpel:privateProperty="true")]', namespaces=common.ns)
for tib_var in tib_vars:
    funcs.get_var_conf(tib_var, wk_dict, num)
    num += 1

flows = proc.xpath('.//bpws:flow', namespaces=common.ns)
# print("flow")
# print(flows)
activities = flows[0].xpath('.//bwext:BWActivity', namespaces=common.ns)
print(activities)

for activity in activities:
    activity_type = activity.attrib['activityTypeID']
    print(activity_type)
    if activity_type == 'bw.generalactivities.timer':
        funcs.get_timer_config(activity, wk_dict)
        num -= 1    
    elif activity_type == 'bw.generalactivities.log':
        funcs.get_log_expr(activity, wk_dict, num)
    num += 1

# Update the output path to use the same name as the input file
out_filepath = os.path.join(current_dir, 'out', f'{base_name}.recipe.json')
os.makedirs(os.path.dirname(out_filepath), exist_ok=True)
with open(out_filepath, 'w') as fout:
    fout.write(json.dumps(wk_dict, indent=4))

zip_path = os.path.join(current_dir, 'out', 'migrated.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    zip_file.write(out_filepath, os.path.basename(out_filepath))

print(f"Migration complete. Output written to {out_filepath} and zipped in {zip_path}")
