## author - sayantan (sayantan.ghosh@strandls.com)
## This script performs migration of StrandOmics code from svn to git repository 

isDropped() {
	isPresent="0"
	for dropped_module in $2
	do
		if [ "$1" == "$dropped_module" ]; then
			isPresent="1"
		else
			continue
		fi
	done
	return $isPresent
}

echo "Starting the migration of modules from svn to git"
shopt -s extglob

ALL_MODULES=$(cat $1)
DROPPED_MODULES=$(cat $2)

ALL_MODULES_COUNT=$(cat $1 | wc -l)
DROPPED_MODULES_COUNT=$(cat $2 | wc -l)

echo "INFO : Modules to be migrated - $ALL_MODULES_COUNT"
echo "INFO : Modules to be dropped from migration - $DROPPED_MODULES_COUNT"

if [[ ! -d svn ]]; then
	mkdir svn
	echo "INFO: Created svn directory"
fi

if [[ ! -d git ]]; then 
	mkdir git
	echo "INFO: Created git directory"
fi

if [[ ! -d logs ]]; then
	mkdir logs
	echo "INFO: Created the logs directory"
fi

cd git
git init
cd ..

DIR=$(pwd)

for module in $ALL_MODULES
do
	isDropped $module $DROPPED_MODULES
	result=$(echo $?)

	if [[ "$result" == "1" ]]; then
		echo "WARNING: $module is getting dropped [see dropped-modules.txt]" | tee -a $LOG_FILE
		echo "INFO: Skipping $module migration" | tee -a $LOG_FILE
		continue
	fi

	LOG_FILE="$DIR/logs/$module.log"
	touch $LOG_FILE

	if [[ ! -f $LOG_FILE ]]; then
		echo "WARNING: Log file creation for $module failed" | tee -a $LOG_FILE
	fi

	cd svn

	echo "INFO: Started cloning of $module from svn repository" | tee -a $LOG_FILE
	git svn clone https://gokarna.strandls.com/svn/rep/comics/$module/ --no-metadata --authors-file=../authors.txt --stdlayout $module/ >> $LOG_FILE 2>&1
	echo "INFO: Successfully cloned the svn repository of $module" >> $LOG_FILE
	echo "INFO: Completed cloning of $module from svn repository" | tee -a $LOG_FILE

	if [[ ! -d $DIR/svn/$module/src && ! -f $DIR/svn/$module/pom.xml ]]; then
		echo "WARNING: No src present in $module cloned repository" | tee -a $LOG_FILE
		echo "INFO: Skipping $module migration" | tee -a $LOG_FILE
		cd ..
		echo -e "\n#####################################\n"
		continue
	fi

	cd $module/
	mkdir $module
	mv !($module) $module
	git add -A 

	echo "INFO: Started committing the contents of $module to sub-folder" | tee -a $LOG_FILE
	git commit -m "Migration from svn to git for $module : Moving to sub-folder" >> $LOG_FILE 2>&1
	echo "INFO: Successfully committed the files for $module" >> $LOG_FILE
	echo "INFO: Completed committing the contents of $module" | tee -a $LOG_FILE

	cd ../../git
	if [[ -d $DIR/svn/$module ]]; then
		git remote add -f $module  $DIR/svn/$module/ >> $LOG_FILE 2>&1
		git merge --no-edit --allow-unrelated-histories $module/master >> $LOG_FILE 2>&1
		echo "INFO: Successfully migrated $module from svn to git repository" | tee -a $LOG_FILE
		echo -e "\n#####################################\n"
	else
		echo "WARNING: $module not present in svn directory" | tee -a $LOG_FILE
	fi
	cd ..
done
