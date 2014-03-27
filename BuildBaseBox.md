# Build a Base Box for Trumpet

## Optional - Build a BaseBox

Install packer 0.5.2

```sh
git clone clone https://github.com/umeboshi2/bento

cd bento/packer

packer build wheezy-i386.json

cd ..

vagrant box add --name wheezy-i386 builds/virtualbox/wheezy-i386.box

```

```sh
cp Vagrantfile.bootstrap Vagrantfile
vagrant up
# Once the bootstrap is complete, package the result
# as a new basebox.  Building nodejs can be time consuming, 
# and only the base system with global node packages and 
# rubygems is installed.  Building a basebox for future use 
# can save a lot of time.
vagrant package
vagrant box add --name trumpet-i386 package.box

```

