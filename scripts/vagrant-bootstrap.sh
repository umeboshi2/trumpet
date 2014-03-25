#!/bin/bash

# add vagrant to staff group to install in /usr/local
adduser vagrant staff

#wget -O - http://debrepos.littledebian.org/littledebian.key | apt-key add -
#wget -O - http://cypress/debrepos/cypress.gpg | apt-key add -



# update package list and upgrade system
apt-get -y update
apt-get -y upgrade

echo "Installing gems"

#gem install sass -v 3.2.9
gem install sass -v 3.2.18
gem install compass -v 0.12.2
gem install susy -v 1.0.9
gem install sassy-buttons -v 0.2.6
gem install bootstrap-sass -v 3.0.2.1
gem install compass-ui -v 0.0.5


#apt-get -y install most python-dev libpq-dev libjpeg62-dev libpng12-dev libfreetype6-dev liblcms1-dev python-requests python-virtualenv libxml2-dev libxslt1-dev

#apt-get -y install rubygems

#apt-get -y install virtualenvwrapper

#apt-get -y install rsync emacs23 screen
#apt-get -y install git-core devscripts


# build deps for nodejs
apt-get -y install cdbs pkg-config

mkdir /tmp/make-nodejs

pushd /tmp/make-nodejs

echo "WARNING: Need to pull or track specific revision"
git clone https://github.com/mark-webster/node-debian

pushd node-debian

node_version=0.10.26
arch=`dpkg --print-architecture`
echo "Node Version: $node_version, arch $arch"

./build.sh $node_version

node_deb=nodejs_$node_version-1_$arch.deb

if [ -f $node_deb ]; then
    echo "Installing $node_deb"
    dpkg -i $node_deb
fi

popd

popd

for package in coffee-script grunt-cli bower ; do
    npm install -g $package
done




echo "Finished with vagrant bootstrap."

