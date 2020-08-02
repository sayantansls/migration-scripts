echo "INFO: OMICS CODE INSTALLATION BEGINS....."

echo "INFO: Updating latest APT Repository"
sudo apt-get update

echo "INFO: Upgrading all the packages to the latest version"
sudo apt-get upgrade

echo "INFO: Installing essentails for building other packages and to have a minimal development environment"
sudo apt install build-essential

cd
echo "INFO: Creating the directory 'installations'"
mkdir tools
cd tools
mkdir installations
cd installations

echo "INFO: Starting the installation for VIM Editor"
echo "INFO: Installing prerequisite libraries for building VIM"

sudo apt install libncurses5-dev libgnome2-dev libgnomeui-dev \
libgtk2.0-dev libatk1.0-dev libbonoboui2-dev \
libcairo2-dev libx11-dev libxpm-dev libxt-dev python-dev \
python3-dev ruby-dev lua5.1 liblua5.1-dev libperl-dev git \
libcanberra-gtk-module libcanberra-gtk3-module

echo "INFO: Fetching VIM Editor"
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

echo "INFO: Checking VIM installation"
vim --version

echo "INFO: Starting the installation for SSH server"
sudo apt install openssh-server

if [[ -f /etc/hosts ]]; then
	echo "INFO: Checking to see /etc/hosts file - File exists"
else
	echo "INFO: Checking to see /etc/hosts file - File does not exist"

echo "INFO: Setting up the omics server hosts in the /etc/hosts file"

sudo echo "192.168.220.27 gokarna.strandls.com" >> /etc/hosts
sudo echo "192.168.220.35	sagara  sagara.strandls.com" >> /etc/hosts
sudo echo "192.168.4.28	batuhi  batuhi.strandls.com" >> /etc/hosts
sudo echo "34.192.114.48   demo    demo.strandomics.com" >> /etc/hosts
sudo echo "10.0.0.13       changuch changuch.strandls.com" >> /etc/hosts

cd ~/tools/installations/

echo "INFO: Starting MySQL installation"
mkdir mysql-installation
cd mysql-installation

echo "INFO: Downloading the MySQL deb pakage"
wget https://dev.mysql.com/get/mysql-apt-config_0.8.3-1_all.deb

echo "INFO: Installing the MySQL deb package"
sudo dpkg -i mysql-apt-config_0.8.3-1_all.deb

sudo apt-get update

sudo apt-get install -y mysql-community-server