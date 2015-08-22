UDACITY-FULLSTACK-NANODEGREE  
PROJECT 3: ITEM CATALOG  
Author: Paul Tai  

Description:
	This application that provides a list of items within a variety of categories
	as well as provide a user registration and authentication system. 
	Registered users will have the ability to post, edit and delete their own items.
    The items themselves fall under two categories, "Cuisines" and "Dishes,
    similar to the restaurant menu app discussed in the python web-apps course.

Project files:
	catalog.py: contains all app-routes and functions
	catalog_db_setup.py: contains the table definitions
	catalog_helpers.py: helpers to generate random strings correct casing
	templates/: contains all of the .html templates used by render_template in catalog.py
	static/: contains a few javascript and image files used by templates

Usage steps:
	If not installed, install Vagrant and VirtualBox.
	
	Clone the git repo containing project files.
		git clone https://github.com/Tyrfang/udacity-fullstack.git
	
	Clone the git repo containing vagrant setup and files
		git clone https://github.com/udacity/fullstack-nanodegree-vm.git
	
	Copy the vagrant folder in this directory into the vagrant folder provided by the Udacity course files
		cp -rf ./udacity-fullstack/project3-item_catalog_results/vagrant/ fullstack-nanodegree-vm/
	
	Navigate to the fullstack-nanodegree-vm/vagrant/
		cd fullstack-nanodegree-vm/vagrant
		
	Boot the viritual machine using Vagrant
		vagrant up
	
	Connect to the virtual machine using Vagrant
		vagrant ssh
	
	Navigate to the sync directory/catalog directory
		cd /vagrant/catalog
	
    Download client_secret.json from the following url and place it in the catalog directory
        https://www.dropbox.com/s/lc7yfjga42vdn6d/client_secret.json?dl=0

	Run catalog.py
        python catalog.py
    
    Connect to the application through a browser at 127.0.0.1:5000
