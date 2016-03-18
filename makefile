OS := $(shell uname)

install_pip:
ifeq ($(OS),Linux)
	apt-get install python-pip python-dev build-essential
endif

install_mongodb:
ifeq ($(OS),Linux)
	apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
	echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
	sudo apt-get update
	sudo apt-get install -y mongodb-org
	service mongod start
endif
ifeq ($(OS),Darwin)
	brew update
	brew install mongodb
	mongod
endif

dependencies:
	$(MAKE) install_pip
	pip install setuptools
	python setup.py install

install:
	$(MAKE) install_mongodb
	$(MAKE) install-without-database

install-without-database:
	$(MAKE) dependencies

test:
	$(MAKE) dependencies
	python setup.py test

run:
	$(MAKE) dependencies
	python -m restAPI