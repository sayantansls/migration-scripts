### Clinician and Hospital Mapping
#### Input file format:
The JSON input file is in the following format:

	{
		"allEmails": ["spassociates6@gmail.com", "mithuaghosh@strandls.com", "spassociates@gmail.com"],
		"contactNumbers": [],
		"email": "spassociates6@gmail.com",
		"faxNumbers": [],
		"hospitals": [{
			"id": 24,
			"contactDetails": {
				"cityID": {
					"uid": "Karnataka_Bengaluru_IN"
				},
				"contactNumbers": [],
				"email": null,
				"faxNumbers": [],
				"postalCode": null,
				"stateName": "karnataka",
				"streetAddress": "HCG Triesta Towers No 8, Kalinga Rao Road, HMT Estate, Sampangiram Nagar"
			},
			"dateCreated": null,
			"hospitalID": {
				"uid": "HL-HCG-627"
			},
			"lastUpdated": "2019-02-08T07:42:03.274Z",
			"name": "HCG, Bangalore",
			"pointOfContact": {
				"firstName": "NA",
				"lastName": null,
				"title": null
			},
			"regionID": {
				"uid": "HCG"
			},
			"status": "ACTIVE",
			"updatedBy": null
		}

#### Output file format:
The pipe-separeted output file is displayed in the following format:

	userName | userEmail | userID | userContactNumbers | hospitalName | hospitalID | streetAddress | cityID | stateName
	Dr. Shekar Patil | spassociates6@gmail.com | 28087faf52c8f0475392dda24f43a917 | NA | HCG, Bangalore | HL-HCG-627 | HCG Triesta Towers No 8, Kalinga Rao Road, HMT Estate, Sampangiram Nagar | Karnataka_Bengaluru_IN | karnataka
	Dr. Shekar Patil | spassociates6@gmail.com | 28087faf52c8f0475392dda24f43a917 | NA | 12345 | HL-IN-10 | NA | NA | NA
	Dr. Shekar Patil | spassociates6@gmail.com | 28087faf52c8f0475392dda24f43a917 | NA | Sri Shankara Cancer Hospital and Research Centre | HL-IN-109 | Basavanagudi, Bangalore 1st Cross,Shankarapuram, Basavanagudi,Landmark:Shankar math, Bangalore | Karnataka_Bengaluru_IN | Karnataka

#### Command to execute

	python clinician_name_hospitals_mapping.py ../data/input/clinicians.json ../data/output/clinician_hospitals_mapping_output.txt > ../data/output/clinician_hospital_mapping.log

Note: Some statistics and the count of one clinician association with number of hospitals are printed into the command line which can be directed into a log file (as shown in the above command).
