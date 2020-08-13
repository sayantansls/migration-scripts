# Migration Script

## Script 1 - 'migrate-svn-to-git.sh'

1. This script is used for the migration of StrandOmics code from svn to git repository (only master)

2. Command to execute:

		./migrate-svn-to-git.sh all-modules.txt dropped-modules.txt

## Script 2 - 'migrate-svn-to-git-branch.sh'

1. This script is used for migration of omics code from svn to git either master or branch (depending on argument provided)

2. Command to execute:

		./migrate-svn-to-git-branch.sh all-modules-6.1.txt dropped-modules.txt [branch-number]

*Note - the first parameter is the file containing the modules to be migrated
		the second parameter is the file containing the modules to be skipped/dropped from migration* 