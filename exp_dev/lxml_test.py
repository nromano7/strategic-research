from lxml import etree
# from pytools import timer

file = './TRIDXML_2018-05-13.xml'

# parse and create DFS iterator for xml document
parser = etree.XMLParser(ns_clean=True, remove_blank_text=True)
xml = etree.parse(file,parser)
tree = xml.iter(tag=etree.Element)

# iterate through tree to get all potential fields and field meta data
xml_dict = {}
for element in tree:
  if element.tag not in xml_dict:
    xml_dict[element.tag] = {
      'parent': None,
      'children': set(),
      'attributes': set(),
    }
  xml_dict[element.tag]['parent'] = element.getparent().tag if element.getparent() else element.getparent()
  xml_dict[element.tag]['children'] = xml_dict[element.tag]['children'].union([child.tag for child in element.getchildren()])
  xml_dict[element.tag]['attributes'] = xml_dict[element.tag]['attributes'].union(element.attrib.keys())

# parse xml wtih lxml.etree
parser = etree.XMLParser(ns_clean=True, remove_blank_text=True)
with timer('lxml.etree'):
  tree = etree.parse(file,parser)
  root = tree.getroot()

# get all child tags of record
all_records = root.xpath('./record')
tags = set()
for record in all_records:
  for element in record:
    tags.add(element.tag)
tags = list(tags)

# get tags for children of record_tags
record_tags = {tag:[] for tag in tags}
for tag in tags:
  dict_child_tags = {}
  set_child_tags = set()
  for child in root.xpath(f'./record/{tag}/*'):
    set_child_tags.add(child.tag)
    set_child_children_tags = set()
    for c in child.getchildren(): 
      # *** only goes three levels deep but some elements have more levels
      set_child_children_tags.add(c.tag)
    dict_child_tags[child.tag] = list(set_child_children_tags)
  if set_child_tags:
    record_tags[tag] = dict_child_tags
  else:
    record_tags[tag] = list(set_child_tags)

with open('tags.txt','w') as f:
  for element in sorted(record_tags):
    f.write(f'{element}\n')
    for elem in record_tags[element]:
      f.write(f'  {elem}\n')
      for e in record_tags[element][elem]:
        f.write(f'    {e}\n')


# def xmltodict(root):
#   contents = []
#   # base case 
#   if len(root) == 0:
#       return
#   # travere each record
#   for child in root:
#     items = {}
#     items['tag'] = child.tag
#     items['attributes'] = child.attrib
#     items['children'] = xmltodict(child)
#     contents.append(items)
#   else:
#     return contents
# contents = xmltodict(root)

# def walk(node):
#   """ iterate tree in pre-order depth-first search order """
#   yield node
#   for child in node.getchildren():
#     for n in walk(child):
#       yield n