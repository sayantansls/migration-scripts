## Most important prequisites
1. Get sudo grant.
2. Have your OS upgraded to the latest version.
3. Get a proper keyboard and mouse.
4. If your PC is wooden forget about the setup.
5. Some of the steps are only valid for Ubuntu Distro >= 16.04

## Get the latest package information
`sudo apt update`

## Upgrade the packagest to their latest updates
`sudo apt upgrade`

## Install essentails for building other packages and to have a minimal development environment
`sudo apt install build-essential`


## Make a directory for installations
`cd ~`
`mkdir installations`


## Install VIM editor (optional)

#### Install prerequisite libraries for building VIM

```bash
sudo apt install libncurses5-dev libgnome2-dev libgnomeui-dev \
libgtk2.0-dev libatk1.0-dev libbonoboui2-dev \
libcairo2-dev libx11-dev libxpm-dev libxt-dev python-dev \
python3-dev ruby-dev lua5.1 liblua5.1-dev libperl-dev git \
libcanberra-gtk-module libcanberra-gtk3-module
```

#### Fetch VIM

```bash
cd ~/installations
mkdir vim
cd vim
git clone https://github.com/vim/vim.git
cd vim
./configure --with-features=huge \
            --enable-multibyte \
	    --enable-rubyinterp=yes \
	    --enable-pythoninterp=yes \
	    --with-python-config-dir=/usr/lib/python2.7/config \
	    --enable-python3interp=yes \
	    --with-python3-config-dir=/usr/lib/python3.6/config \
	    --enable-perlinterp=yes \
	    --enable-luainterp=yes \
            --enable-gui=gtk2 \
            --enable-cscope \
	   --prefix=/usr/local

make
sudo make install
```

##### Check the VIM version

```bash
vim --version
```

gvim should also has been installed


#### Reference
[YouCompleteMe guide](https://github.com/ycm-core/YouCompleteMe/wiki/Building-Vim-from-source)

## Install SSH server
`sudo apt install openssh-server`

#### Add some important host names for convenient addressing.
```bash
sudo vim /etc/hosts

# Add the following after your system host name
192.168.220.27 gokarna.strandls.com
192.168.220.35	sagara  sagara.strandls.com
192.168.4.28	batuhi  batuhi.strandls.com
34.192.114.48   demo    demo.strandomics.com
10.0.0.13       changuch changuch.strandls.com
```

This is to access the machines using the host name directly instead of ip address

## Install MySQL
```bash
cd ~/installations
mkdir mysql_installation
```

#### Download MySQL APT Repository
Go to [link](https://dev.mysql.com/downloads/repo/apt/) and download the deb package in to the current directory
Add it to the repositories `sudo dpkg -i /PATH/version-specific-package-name.deb`
Now refresh the repositories `sudo apt update`


#### Install
`sudo apt install mysql-server` and go with defaults

See [Installation guide using apt](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/).

#### Note
you can also update the MySQL from src in any custom directory. But for tracking its updates it better to install
from apt. See [Install from source](https://dev.mysql.com/doc/refman/8.0/en/installing-source-distribution.html) for manual installation.


#### Adding a new User
Add a user instead of going with root always and for JDBC permissions (Executing the SQL queries from JAVA).

Open mysql cli
`mysql -u root -p`
Enter the root password that you have set up.

For security reasons, user name and password are not included in this page.

```sql
CREATE USER 'XXXXXXXX'@'localhost' IDENTIFIED BY 'YYYYYYYY'; # Ask any developer for the password to be set in the place of YYYYYYY and user name in place of XXXXXXXXXXX
GRANT ALL PRIVILEGES ON * . * TO 'XXXXXXXXX'@'localhost'; # Grant all the permissions for the user
```

Exit the cli using _Ctrl + D_

For reference see [Adding users](https://dev.mysql.com/doc/refman/8.0/en/creating-accounts.html)


#### Changing MySQL data directory
We have hundreds of GB data in Omics and the default data directory for MySQL is **/var/lib/mysql/**

Many of us may not have that amount of space in the /var partition. So its better to point it to some directory in the home folder.

`cd ~`
`mkdir mysql_data # Lets put the data here`

###### Stop Mysql
`sudo systemctl stop mysql`

Make sure that it is stopped `sudo systemctl status mysql`


###### Sync the data
`sudo rsync -av /var/lib/mysql mysql_data/`

##### Delete or rename the old dir
`sudo mv /var/lib/mysql /var/lib/mysql.bak`

#### Point the new Directory
`sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf`

Change __datadir__ to the new location i.e., `/home/<user>/mysql_data/mysql`


#### Change the security profile of MySQL

Method 1: Add alias
Add `alias /var/lib/mysql/ -> /home/<user>/mysql_data/mysql/,` in /etc/apparmor.d/tunables/alias
Method 2: Change the profile directly
In /etc/apparmor.d/usr.sbin.mysqld change /var/lib/mysql to the new path

Restart apparmor
`sudo systemctl restart apparmor`

##### Keep a dummy directory for start validations
`sudo mkdir /var/lib/mysql/mysql -p`

#### Start mysql
`sudo systemctl start mysql`
Check status
`sudo systemctl status mysql`


#### Check if the new data directory is reflected
`mysql -u <user> -p`
Run `select @@datadir;`

Reference [changing data dir](https://www.digitalocean.com/community/tutorials/how-to-move-a-mysql-data-directory-to-a-new-location-on-ubuntu-16-04)

#### Fetching the data

Take all the schema dumps of databases from a server and dump them to your local data bases.

Example: 
Taking dump : `mysqldump -u strand -pxxxxxxxxx --no-data  comicsDB > comicsDB.sql`
Applying dump : `mysql -u strand -p comicsDB < comicsDB.sql`



## Installing Redis
`cd ~/installations`
`mkdir redis`
`cd redis`
Go download from [redis](https://redis.io/download) and follow the install instructions
`make`
`cd src`
`./redis-server &`

#### Disable protected mode
`./redis-cli`
`CONFIG SET protected-mode no`




## Installing subversion
Chances are that it is pre installed.

In case it is not installed already,

Note that you only need to install the svn client. 

`sudo apt install subversion`


## Fetching the repository
```bash
cd ~
mkdir rep
cd rep
svn co https://gokarna.strandls.com/svn/rep/comics/ -N # Only the sparse files
svn co https://gokarna.strandls.com/svn/rep/tools/

cd comics

python svntrunk.py up
```


## Setting up IDE. choose either eclipse or intellij
## Intellij Setup

Download from [link](https://www.jetbrains.com/idea/download/download-thanks.html?platform=linux)

```bash
cd ~/installations
mkdir intellij
cd intellij
mv ~/Downloads/ideaxxxxxx .
tar -xvf ideaxxxxx
cd ideaxxxxxx/bin
./idea # and follow the steps
```


## Install Java

Find a downloaded jdk-8 from somewhere or buy it from oracle.
Unzip it and set 

```bash
export JAVA_HOME=/usr/java/<your version of java>
export PATH=${PATH}:${JAVA_HOME}/bin
```

in your ~/.bashrc


optionally,

`sudo update-alternatives --install /usr/bin/java java /home/hari/installations/java/jdk1.8.0_202/bin/java 1`


## Install maven
Download from [apache](https://maven.apache.org/download.cgi) and follow instructions from [install](https://maven.apache.org/install.html)

#### Add gokarna credentials for maven
get settings.xml from some one from their ~/.m2 directory and copy it to yours. If the directory is not present create one



## Test the build
Now that mvn and java are installed lets test the build

```bash
cd ~/rep/comics
./build.sh
```

It should be successful

## Import project to Intellij

Launch idea and import project and import entire rep folder. Set maven import and search for projects recursively.

## Install Tomcat
Download a binary distribution from [apache](https://tomcat.apache.org/download-80.cgi) and extract it.


### Set tomcat in intellij
Open file context.xml in webapp. Use `ctrl + shif + N`

Copy context.xml from any developer to make sure you have the latest version and replace it with yours.