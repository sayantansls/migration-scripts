"""
author : sayantan (sayantan.ghosh@strandls.com)
This script consumes a JSON file containing user email data and 
creates a TSV file of the desired format
"""

import time as tm
import re
from collections import defaultdict
import sys, copy, os

HEADERS = ['email_id',
		   'mapped_ids',
		   'mapped_ids_count',
		   'is_blocked']

ENTRY_T = {'email_id': '',
		   'mapped_ids': '',
		   'mapped_ids_count': '',
		   'is_blocked': ''}

sep = '\t'

def create_blocked_list(blocked_file):
	blocked_list = list()
	f = open(blocked_file, 'r')
	for line in f.readlines():
		blocked_list.append(line.strip('\n'))
	return blocked_list

def remove_unwanted_keys(line):
	date1 = re.findall(r'"dateCreated" : ISODate\(.*?\), ', line)[0]
	date2 = re.findall(r'"lastUpdated" : ISODate\(.*?\), ', line)[0]
	store_boolean = re.findall(r'"storePersistently" : .*?, ', line)[0]
	new_line = line.replace(date1, '').replace(date2, '').replace(store_boolean, '')
	return new_line

def process_entries(email_file, output):
	id_to_email = dict()
	f = open(email_file, 'r')
	for line in f.readlines():
		number_id_list = re.findall(r'NumberLong\(\d+\)', line)
		for number_id in number_id_list:
			str_number_id = '"' + number_id + '"'
			str_line = line.replace(number_id, str_number_id)
			line = str_line
			
		dict_line = remove_unwanted_keys(str_line)
		line_dict = eval(dict_line)
		id_to_email[line_dict['_id']] = line_dict['email']['bcc'] + line_dict['email']['to']

	email_to_id = defaultdict(list)
	for key, value in id_to_email.items():
		for email in value:
			email_to_id[email].append(key)

	for key, value in email_to_id.items():
		ENTRY = copy.deepcopy(ENTRY_T)

		ENTRY['email_id'] = key
		ENTRY['mapped_ids'] = value
		ENTRY['mapped_ids_count'] = len(value)
		ENTRY['is_blocked'] = "N/A"

		field_values = [str(ENTRY[i]) for i in HEADERS]
		output.write(sep.join(field_values))
		output.write('\n')

def main(email_file):
	print("Start of code:", tm.ctime(tm.time()))

	filename = os.path.basename(email_file)
	output_file = filename.replace('.json','_out.tsv')

	output = open(output_file, 'w')
	output.write(sep.join(HEADERS))
	output.write('\n')

	process_entries(email_file, output)

	print("End of code:", tm.ctime(tm.time()))

if __name__ == '__main__':
	main(sys.argv[1])