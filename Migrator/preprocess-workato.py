import json

in_file = 'a000_helloworld.recipe.json'
out_file = 'Processed_' + in_file
in_file_path = './in/' + in_file
out_file_path = './in/' + out_file

with open(in_file_path, 'r') as f:
    wk_dict = json.load(f)

if wk_dict.get('code').get('dynamicPickListSelection') != None:
    wk_dict['code'].pop('dynamicPickListSelection')
if wk_dict.get('code').get('extended_input_schema') != None:
    wk_dict['code'].pop('extended_input_schema')
if wk_dict.get('code').get('extended_output_schema') != None:
    wk_dict['code'].pop('extended_output_schema')
if wk_dict.get('code').get('block')[0].get('extended_input_schema') != None:
    wk_dict['code']['block'][0].pop('extended_input_schema')
if wk_dict.get('code').get('block')[0].get('extended_output_schema') != None:
    wk_dict['code']['block'][0].pop('extended_output_schema')

#with open(out_file_path, 'w') as f:
    #f.write(json.dumps(wk_dict, indent=4))