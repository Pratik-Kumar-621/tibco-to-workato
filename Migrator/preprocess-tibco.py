from lxml import etree

in_file = 'Process.bwp'
out_file = 'Processed_' + in_file
in_file_path = './in/' + in_file
out_file_path = './in/' + out_file
ns = {'notation': 'http://www.eclipse.org/gmf/runtime/1.0.2/notation'}

el = etree.parse(in_file_path)
proc = el.getroot()
for diagram in proc.xpath('//notation:Diagram', namespaces = ns):
    diagram.getparent().remove(diagram)

with open(out_file_path, 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + etree.tostring(el, encoding=str))