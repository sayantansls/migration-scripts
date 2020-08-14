# Parse Context XML File

## Definition
This script consumes a context.xml file and prints out all the data in TSV format.

## Execution
1. Input -- The input file is a 'context.xml' file.
2. Output -- There are two output files - one capturing all the data from the 'Environment' child tags and one for 'Resource' child tags. The files are tab-separated format (TSV) files. The output files are stored in the location - */parse-context-xml/data/output/*.
3. Command to execute --

		python parse-context-xml.py [input context.xml file]

## Contact

Author - Sayantan Ghosh (sayantan.ghosh@strandls.com)