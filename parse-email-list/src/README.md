# Parse Oms-Omics Email List

## Definition

Script to parse through json file containing email and other definitions and creating a TSV file 

## Inputfile format

The format of the input file is as follows:

	{ "_id" : NumberLong(279658), "email" : { "attachments" : [ ], "bcc" : [ "rashi.tomar@strandls.com", "caren@strandls.com", "aishwarya.ramkumar@strandls.com" ], "body" : "New activity is created. Details follow:<br/>Test Request ID: STRAN-2018-8230<br/>Product: Strand Neurodevelopmental Disorders Test<br/>Panel: TsoT1<br/><b>Update Activity:</b><br/>Register Sales Order (Status: Signed off)<br/><b>Current Activity:</b><br/>Update Sales Order (Status: Ready).<br/><br/>Click <a href=\"https://clinical.strandomics.com/oms/index\">here</a> to check all the activities assigned to you.", "cc" : [ ], "emailID" : { "_class" : "EmailID", "uid" : "Email_400587" }, "replyTo" : [ ], "sender" : { "_class" : "UserID", "uid" : "USER_545" }, "subject" : "New activity Update Sales Order (Status: Ready) created for test request STRAN-2018-8230 and product Strand Neurodevelopmental Disorders Test", "to" : [ ] }, "failedDeliveryCount" : 1, "queuedEmailID" : { "_class" : "QueuedEmailID", "uid" : "Email_400587" }, "storageIDs" : [ ], "version" : NumberLong(0) }


## Outputfile format

	email_id	mapped_ids	mapped_ids_count	is_blocked
	shruti@strandls.com	['NumberLong(522248)']	1	False
	moon.sung@sanomics.com	['NumberLong(523922)', 'NumberLong(521593)', 'NumberLong(523307)', 'NumberLong(522832)', 'NumberLong(521943)', 'NumberLong(524121)']	6	False
	sunitha@strandls.com	['NumberLong(523217)', 'NumberLong(522857)', 'NumberLong(523890)', 'NumberLong(523362)', 'NumberLong(522907)', 'NumberLong(522248)', 'NumberLong(522268)', 'NumberLong(522882)', 'NumberLong(523287)', 'NumberLong(522188)', 'NumberLong(522932)', 'NumberLong(523042)']	12	False


## Command to run

	python parse_email_list.py inputfile.json

[A TSV output file with the same name as the inputfile with the suffix '\_out' will be created in the same directory]

## Contact

Author : Sayantan Ghosh (sayantan.ghosh@strandls.com)