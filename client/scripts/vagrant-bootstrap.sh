#!/bin/bash

# add vagrant to staff group to install in /usr/local
adduser vagrant staff

#wget -O - http://debrepos.littledebian.org/littledebian.key | apt-key add -
#wget -O - http://cypress/debrepos/cypress.gpg | apt-key add -



# update package list and upgrade system
apt-get -y update
apt-get -y upgrade

_python_dev="python-dev libpq-dev libjpeg62-dev libpng12-dev libfreetype6-dev liblcms1-dev python-requests python-virtualenv libxml2-dev libxslt1-dev virtualenvwrapper"

_misc_stuff="emacs23 screen git-core devscripts cdbs pkg-config most"

_apache_stuff="libapache2-mod-wsgi apache2-mpm-worker apache2-utils apache2"

_ruby_stuff="rubygems"

debpackages="$_python_dev $_misc_stuff $_apache_stuff $_ruby_stuff"

echo "Installing debian packages: $debpackages"

apt-get -y install $debpackages


echo "Installing gems"

gem install sass -v 3.2.18
gem install compass -v 0.12.2
gem install susy -v 1.0.9
gem install sassy-buttons -v 0.2.6
gem install bootstrap-sass -v 3.0.2.1
gem install compass-ui -v 0.0.5

echo "Preparing to build nodejs"

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
    echo "Moving $node_deb to /root"
    mv -i $node_deb /root
fi

popd

popd

for package in coffee-script grunt-cli bower ; do
    npm install -g $package
done

echo "finished installing node packages."

echo "Performing cleanup"

rm -fr /tmp/make-nodejs

apt-get -y autoremove
apt-get -y clean


echo "Creating large file to clean drive for packing."

dd if=/dev/zero of=/EMPTY bs=1M
rm -f /EMPTY
sync


echo "Finished with vagrant bootstrap."

