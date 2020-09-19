"""
author : sayantan (sayantan.ghosh@strandls.com)
This script contains the utility functions being used by the other scripts
"""

import os, json 

def check_file_exists(input_file):
	if not os.path.exists(input_file):
		raise Exception(messages['error-messages']['FILE_NOT_PRESENT'].format(input_file))

def read_json(json_file):
	check_file_exists(json_file)
	return json.load(open(json_file, 'r'))

def read_properties(prop_file):
	check_file_exists(prop_file)
	properties_map = dict()
	for line in open(prop_file, 'r').readlines():
		key, value = line.split('=')
		if key not in properties_map:
			properties_map[key] = value.strip()
	return properties_map

config_json = read_json('../data/config.json')
messages = read_json(config_json['messages-file'])
