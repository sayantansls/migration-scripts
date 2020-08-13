## author - sayantan (sayantan.ghosh@strandls.com)
## This script performs migration of StrandOmics code from svn to git repository
## If 'branch number' (eg. 6.1) is given as the third argument then it will trigger creation of 6.1 branch

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

shopt -s extglob
BRANCH="$3"

if [[ ! -z $BRANCH ]]; then
	echo "INFO : Starting the migration of branch $BRANCH from svn to git"
	SVN_DIR="svn-$BRANCH"
	GIT_DIR="git-$BRANCH"
	LOG_DIR="logs-$BRANCH"
	COMMIT_MESSAGE="Migration from svn to git branch 6.1 : Moving to sub-folder"
else
	echo "INFO : Starting the migration of modules from svn to git"
	SVN_DIR="svn"
	GIT_DIR="git"
	LOG_DIR="logs"
	COMMIT_MESSAGE="Migration from svn to git : Moving to sub-folder"
fi

ALL_MODULES=$(cat $1)
DROPPED_MODULES=$(cat $2)

ALL_MODULES_COUNT=$(cat $1 | wc -l)
DROPPED_MODULES_COUNT=$(cat $2 | wc -l)

echo "INFO : Modules to be migrated - $ALL_MODULES_COUNT"
echo "INFO : Modules to be dropped from migration - $DROPPED_MODULES_COUNT"

if [[ ! -d $SVN_DIR ]]; then
	mkdir $SVN_DIR
	echo "INFO : Created $SVN_DIR directory"
fi

if [[ ! -d $GIT_DIR ]]; then 
	mkdir $GIT_DIR
	echo "INFO : Created $GIT_DIR directory"
fi

if [[ ! -d $LOG_DIR ]]; then
	mkdir $LOG_DIR
	echo "INFO : Created $LOG_DIR directory"
fi

cd $GIT_DIR
if [[ ! -d .git ]]; then
	git init
	echo "INFO : Initialized git repository"
fi
cd ..

DIR=$(pwd)

for module in $ALL_MODULES
do
	isDropped $module $DROPPED_MODULES
	result=$(echo $?)

	if [[ "$result" == "1" ]]; then
		echo "WARNING : $module is getting dropped [see dropped-modules.txt]" | tee -a $LOG_FILE
		echo "INFO : Skipping $module migration" | tee -a $LOG_FILE
		continue
	fi

	LOG_FILE="$DIR/$LOG_DIR/$module.log"
	touch $LOG_FILE

	if [[ ! -f $LOG_FILE ]]; then
		echo "WARNING : Log file creation for $module failed" | tee -a $LOG_FILE
	fi

	cd $SVN_DIR

	echo "INFO : Started cloning of $module from svn repository" | tee -a $LOG_FILE
	git svn clone https://gokarna.strandls.com/svn/rep/comics/$module/ --no-metadata --authors-file=../authors.txt --stdlayout $module/ >> $LOG_FILE 2>&1
	echo "INFO : Successfully cloned the svn repository of $module" >> $LOG_FILE
	echo "INFO : Completed cloning of $module from svn repository" | tee -a $LOG_FILE

	if [[ ! -d $DIR/$SVN_DIR/$module/src && ! -f $DIR/$SVN_DIR/$module/pom.xml ]]; then
		echo "WARNING : No src present in $module cloned repository" | tee -a $LOG_FILE
		echo "INFO : Skipping $module migration" | tee -a $LOG_FILE
		cd ..
		echo -e "\n#####################################\n"
		continue
	fi

	cd $module/
	mkdir $module

	if [[ ! -z $BRANCH ]]; then
		git checkout -b $BRANCH origin/$BRANCH
	fi	

	mv !($module) $module
	git add -A 

	echo "INFO : Started committing the contents of $module to sub-folder" | tee -a $LOG_FILE
	git commit -m "$COMMIT_MESSAGE" >> $LOG_FILE 2>&1
	echo "INFO : Successfully committed the files for $module" >> $LOG_FILE
	echo "INFO : Completed committing the contents of $module" | tee -a $LOG_FILE

	cd ../../$GIT_DIR
	if [[ -d $DIR/$SVN_DIR/$module ]]; then
		git remote add -f $module  $DIR/$SVN_DIR/$module/ >> $LOG_FILE 2>&1
		git merge --no-edit --allow-unrelated-histories $module/$BRANCH >> $LOG_FILE 2>&1
		echo "INFO : Successfully migrated $module from svn to git repository" | tee -a $LOG_FILE
		echo -e "\n#####################################\n"
	else
		echo "WARNING : $module not present in svn directory" | tee -a $LOG_FILE
	fi
	cd ..
done
