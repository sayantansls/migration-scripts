"""
author : sayantan (sayantan.ghosh@strandls.com)
The script consumes a JSON file and creates a TSV file to map a clinician to the hospital
"""
import time as tm
import json, copy
import sys, os

HEADERS = ['userName',
           'userEmail',
           'userID',
           'userContactNumbers',
           'hospitalName',
           'hospitalID',
           'streetAddress',
           'cityID',
           'stateName']

ENTRY_T = {'userName': '',
           'userEmail': '',
           'userID': '',
           'userContactNumbers': '',
           'hospitalName': '',
           'hospitalID': '',
           'streetAddress': '',
           'cityID': '',
           'stateName': ''}

sep = ' | '

def check_null(value):
    if value is None:
        return 'NA'
    else:
        return value.replace('\n','')

def validate_contact_info(contactNumbers):
    if len(contactNumbers) == 0:
        return 'NA'
    else:
        return ','.join(contactNumbers)

def validate_uid(id_dict):
	try:
		return id_dict['uid']
	except:
		return 'NA'

clinician_set, hospital_set = [set(), set()]

def process_entries(json_list, output):
	for entry in json_list:
		ENTRY = copy.deepcopy(ENTRY_T)
		userName = entry['username']
		ENTRY['userName'] = userName
		clinician_set.add(userName)

		ENTRY['userEmail'] = entry['email']
		ENTRY['userID'] = validate_uid(entry['userID'])
		ENTRY['userContactNumbers'] = validate_contact_info(entry['contactNumbers'])
		hospital_list = entry['hospitals']
		print("{} mapped to {} hospital(s)".format(userName.encode('utf-8'), len(hospital_list)))
		for hospital in hospital_list:
			hospitalName = hospital['name']
			ENTRY['hospitalName'] = hospitalName
			hospital_set.add(hospitalName)

			ENTRY['streetAddress'] = check_null(hospital['contactDetails']['streetAddress'])
			ENTRY['cityID'] = validate_uid(hospital['contactDetails']['cityID'])
			ENTRY['hospitalID'] = validate_uid(hospital['hospitalID'])

			ENTRY['stateName'] = check_null(hospital['contactDetails']['stateName'])
			print("{} mapped to the hospital {}".format(userName.encode('utf-8'), hospitalName.encode('utf-8')))

			field_values = [ENTRY[i].encode('utf-8') for i in HEADERS]
			output.write(sep.join(field_values))
			output.write('\n')
		print("--"*50)

def main(input_file, output_file):
    print("Start of code:", tm.ctime(tm.time()))
    with open(input_file) as f:
        data = json.loads(f.read())

    output = open(output_file, 'w')
    output.write(sep.join(HEADERS))
    output.write('\n')

    print('Mapping the clinicians to their respective hospitals')
    print('Input File : {}'.format(input_file))
    print('Output File : {}'.format(output_file))
    process_entries(data, output)
    print('#Unique Number of clinicians {}'.format(len(clinician_set)))
    print('#Unique Number of hospitals {}'.format(len(hospital_set)))

    print("End of code:", tm.ctime(tm.time()))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
