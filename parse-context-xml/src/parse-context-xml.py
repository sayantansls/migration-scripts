"""
author : sayantan (sayantan.ghosh@strandls.com)
This script consumes the omics context.xml file and 
shares the data in a flat format and points out statistics and duplications 
in the given xml file.
"""

import time as tm
import xml.etree.ElementTree as ET
import sys, copy, os
from pprint import pprint

def compare_children(children):
	# children is a list of dictionaries
	is_same, duplicated_tags = [0, list()]
	for child in children:
		compare_set = copy.deepcopy(children)
		compare_set.remove(child)
		# compare_set has all the dictionaries except the one being compared
		for item in compare_set:
			if item.keys().sort() == child.keys().sort():
				if cmp(item, child) == 0:
					duplicated_tags.append(child)
	print('Number of duplicated child tags : {}'.format(len(duplicated_tags)))
	pprint(duplicated_tags)
	
def segregate_child(children):
	type_dict = dict()
	for child in children:
		for tag_type in child_types:
			if child.tag == tag_type:
				if not tag_type in type_dict:
					type_dict[tag_type] = 0
				type_dict[tag_type] += 1
	return type_dict

def print_out_xml(children, output):
	headers = children[0].keys()
	
	#for child in children:
		#print('\t'.join(child.keys()))

	#output.write('\t'.join(headers))
	#output.write('\n')

	for child in children:
		output.write('\t'.join(child.values()))
		output.write('\n')

def main(xml_file):
	print('Start of code : {}'.format(tm.ctime(tm.time())))

	tree = ET.parse(xml_file)
	root = tree.getroot()

	global child_types
	child_types, children = [set(), list()]
	children_env, children_res = [list(), list()]
	env_tags, res_tags = [0, 0]
	for child in root:
		child_types.add(child.tag)
		children.append(child.attrib)

		if child.tag == 'Environment':
			children_env.append(child.attrib)
		elif child.tag == 'Resource':
			children_res.append(child.attrib)

	output_filename = xml_file.replace('.xml', '-output-res.tsv')
	output_path = os.path.join('../data/output', os.path.basename(output_filename))
	output = open(output_path, 'w+') 
	print_out_xml(children_res, output)

	print('Number of child tags : {}'.format(len(root)))
	print('Type of child tags : {}'.format(child_types))
	tag_distribution = segregate_child(root)
	print('Child Tag distribution : {}'.format(tag_distribution))
	compare_children(children)
	print('End of code : {}'.format(tm.ctime(tm.time())))


if __name__ == '__main__':
	main(sys.argv[1])