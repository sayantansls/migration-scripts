"""
author : sayantan (sayantan.ghosh@strandls.com)
This script performs the processes required for reported variants reclassification
upto the creation of VCFs which are to be uplaoded to StrandOmics
"""

import csv, sys, json
import os, utils

config_json = utils.read_json('../data/config.json')
messages = utils.read_json(config_json['messages-file'])

INPUT_DIR, OUTPUT_DIR = [config_json['input-dir'], config_json['output-dir']]

class CaseIdTestIdMafObject():
	def __init__(self, test_id, case_id, maf):
		self.case_id = case_id
		self.test_id = test_id
		self.maf = maf

	def toString(self):
		print('CASE ID : {} ; TEST ID : {} ; MAF : {}'.format(self.case_id, self.test_id, self.maf)) 

"""
The headers in the file test-details.tsv file are as follows:
0  -- test_id	                1  -- test_name	          2  -- display_name	
3  -- description	            4  -- test_scope	      5  -- incidental_finding_preference	
6  -- test_type	                7  -- test_status	      8  -- panel_id	
9  -- expected_turnaround_time  10 -- coverage_threshold  11 -- allele_frequency	
12 -- created_by	            13 -- creation_time	      14 -- modification_time	
15 -- facility_id	            16 -- show_panel_genes
"""

def create_map_from_file(file_object):
	file_map = dict()
	if not os.path.exists(file_object['file']):
		raise Exception(messages['error-messages']['FILE_NOT_PRESENT'].format(file_object['file']))
	input_file = open(file_object['file'], 'r')
	input_data = csv.DictReader(input_file, delimiter='\t', dialect=csv.excel_tab)
	for row in input_data:
		if not row[file_object['key_field']] in file_map:
			file_map[row[file_object['key_field']]] = row[file_object['value_field']]
	return file_map

def create_caseid_testid_maf_objects(test_id_maf_map, test_id_case_id_map):
	all_tests = test_id_maf_map.keys()
	global caseid_testid_maf_objects
	caseid_testid_maf_objects, failed_tests = [list(), set()]
	for test in all_tests:
		try:
			caseid_testid_maf_object = CaseIdTestIdMafObject(test, test_id_case_id_map[test], test_id_maf_map[test])
		except:
			failed_tests.add(test)
			
		caseid_testid_maf_objects.append(caseid_testid_maf_object)

	if failed_tests:
		print(messages['success-messages']['TEST_ABSENT'].format(len(failed_tests)))

"""
The headers in the case_registry.tsv file are as follows:
0  -- case_no	         1  -- case_alias	                   2  -- test_id	
3  -- gene_list_id	     4  -- case_type	                   5  -- case_class	
6  -- clinical_summary	 7  -- phenotype_list	               8  -- specimen_type	
9  -- case_notes	     10 -- incidental_finding_preference   11 -- case_status	
12 -- activation_status	 13 -- created_by	                   14 -- creation_time	
15 -- modification_time	 16 -- case_ready_for_analysis_time	   17 -- case_due_time	
18 -- facility_id	     19 -- configuration_id	               20 -- message
"""

def map_maf_to_reported_variants(reported_variants_dump, output):
	input_file = open(reported_variants_dump, 'r')
	input_data = csv.DictReader(input_file, delimiter='\t')
	field_names = input_data.fieldnames
	field_names.append('MAF')

	output_file = open(output, 'w+')
	output_writer = csv.DictWriter(output_file, delimiter='\t', fieldnames=field_names)
	output_writer.writeheader()

	maf_for_row, failed_mapping = ['Not found', set()]
	for row in input_data:
		for obj in caseid_testid_maf_objects:
			if row['Case ID'].strip() == obj.case_id:
				maf_for_row = obj.maf
		if maf_for_row == 'Not found' : failed_mapping.add(row['Case ID'])
			
		row['MAF'] = maf_for_row
		output_writer.writerow(row)

	if failed_mapping: print(messages['success-messages']['CASES_MAF_FAIL'].format(len(failed_mapping)))

def split_file_on_maf(reported_variants_dump):
	maf_types = config_json['maf-types']
	output_files = list()
	for maf_type in maf_types:
		input_file = open(reported_variants_dump, 'r')
		input_data = csv.DictReader(input_file, delimiter='\t')
		field_names = input_data.fieldnames

		output = reported_variants_dump.replace('.tsv', '-{}.tsv'.format(maf_type))
		output_files.append(output)
		print(messages['success-messages']['FILE_WRITE'].format(maf_type, output))
		output_file = open(output, 'w+')
		output_writer = csv.DictWriter(output_file, delimiter='\t', fieldnames=field_names)
		output_writer.writeheader()

		for row in input_data:
			if row['MAF'].strip() == maf_type:
				output_writer.writerow(row)

	return output_files

"""
The headers in the reported-variants-dump files are as follows:
0  -- Case ID	        1  -- UK1	           2  -- UK2	                 3  -- Panel
4  -- Test	            5  -- Date and Time	   6  -- UK3	                 7  -- Gender
9  -- Ethnicity	        10 -- Age	           11 -- ReportWiseGeneListInfo  12 -- UK4
13 -- UK5	            14 -- UK6	           15 -- Chromosome	             16 -- Gene
17 -- c.HGVS/p.HGVS	    18 -- Genomic HGVS	   19 -- Transcript	             20 -- Variant Type
21 -- Allele Frequency	22 -- Global PPDB	   23 -- Local PPDB	             24 -- Zygosity
25 -- Clinvar Ids	    26 -- Variant Label	   27 -- Variant Label Reason	 28 -- rsIDs
29 -- EVS	            30 -- ExAC	           31 -- dbSNP	                 32 -- 1000 Genomes
33 -- HGMD ID	        34 -- Bioinfo Summary  35 -- Literature Summary	     36 -- UK7
37 -- UK8	            38 -- UK9	           39 -- UK10	                 40 -- UK11
41 -- UK12	            42 -- UK13	           43 -- UK14	                 44 -- UK15	
45 -- UK16	            46 -- UK17	           47 -- UK18                    48 -- MAF
"""

def create_input_files_for_vcf_creation(reported_variants_dump):
	headers = ['Gene name', 'genomicHGVS']
	input_file = open(reported_variants_dump, 'r')
	input_data = csv.DictReader(input_file, delimiter='\t')

	output_file = open(reported_variants_dump.replace('.tsv', '-for-vcf.tsv'), 'w+')
	output_file.write('\t'.join(headers))
	output_file.write('\n')

	for row in input_data:
		field_values = row['Gene'] + '\t' + row['Genomic HGVS'] 
		output_file.write(field_values)
		output_file.write('\n')

def main(test_details, case_registry, reported_variants_dump):
	test_details_object = {'file' : test_details, 'key_field' : 'test_id', 'value_field' : 'allele_frequency'}
	case_registry_object = {'file' : case_registry, 'key_field' : 'test_id', 'value_field' : 'case_no'}
	
	test_id_maf_map = create_map_from_file(test_details_object)
	if test_id_maf_map:
		print(messages['success-messages']['TEST_MAF_MAP_SUCCESS'])
	else:
		raise Exception(messages['error-messages']['TEST_MAF_MAP_FAIL'])

	test_id_case_id_map = create_map_from_file(case_registry_object)
	if test_id_case_id_map:
		print(messages['success-messages']['TEST_CASE_MAP_SUCCESS'])
	else:
		raise Exception(messages['error-messages']['TEST_CASE_MAP_FAIL'])

	create_caseid_testid_maf_objects(test_id_maf_map, test_id_case_id_map)
	output = reported_variants_dump.replace('.tsv', '-output.tsv').replace(INPUT_DIR, OUTPUT_DIR)
	map_maf_to_reported_variants(reported_variants_dump, output)

	if os.path.exists(output):
		print(messages['success-messages']['OUTPUT_PRESENT'].format(output))
	else:
		raise Exception(messages['error-messages']['OUTPUT_ABSENT'])

	split_files = split_file_on_maf(output)
	for file in split_files:
		if not os.path.exists(file):
			raise Exception(messages['error-messages']['SPLIT_FILE_ABSENT'].format(file))
		else:
			print(messages['success-messages']['SPLIT_FILE_PRESENT'].format(file))
			create_input_files_for_vcf_creation(file)
			print(messages['success-messages']['VCF_INPUT_FILE'].format(file))

if __name__ == '__main__':
	properties = utils.read_properties(config_json['properties-file'])
	main(properties['test-details'], properties['case-registry'], properties['reported-variants-dump'])