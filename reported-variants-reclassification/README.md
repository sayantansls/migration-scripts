# Reported Variants Reclassification

## Process
1. There are three files required - **test-details.tsv**, **reported-variants-dump.tsv**, **case_registry.tsv**
	* test-details.tsv --> dump TSV file required from clinical database
	* reported-variants-dump.tsv --> dump TSV file required from clinical database
	* case_registry.tsv --> dumpf of MySQL table case_registry from database '' required from clinical database
2. The file case_registry provides a mapping of Case ID to the Test ID.
3. The file test details provides a mapping of Test ID to allele frequency (MAF).
4. On combining, these mappings we can assign MAF to the Case IDs present in the reported-variants-dump.tsv file.
5. Split the reported-variants-dump.tsv file into 3 files based on the MAF values - **0.01**, **0.02** and **0.05**.

## Implementation

## Execution

## Limitations

## Contact

Author - Sayantan Ghosh (sayantan.ghosh@strandls.com)