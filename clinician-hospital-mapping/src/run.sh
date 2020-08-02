## This is the shell script to run the cinician name to hospital mapping

echo "Running the clinician-hospital mapping script"
echo "Input : ../data/input/clinicians.json"
echo "Output : ../data/output/clinician_hospitals_mapping_output.txt"
echo "Log : ../data/output/clinician_hospital_mapping.log"

python clinician_name_hospitals_mapping.py ../data/input/clinicians.json ../data/output/clinician_hospitals_mapping_output.txt > ../data/output/clinician_hospital_mapping.log

echo "INFO : Script run successfully [to change the input, output or log parameters change the parameters in the run.sh script (See README.md for more details)]"