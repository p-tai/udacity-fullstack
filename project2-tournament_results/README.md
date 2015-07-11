UDACITY-FULLSTACK-NANODEGREE  
PROJECT 2: TOURNAMENT DATABASE  
Author: Paul Tai

Description:
	This program assists in the recording and pairing of tournament
	participants following a swiss-style tournament format.

Project files:  
	tournament.py: API for using the underlying Tournaments database.  
		- registerPlayer(name)  
		- countPlayers()  
		- deletePlayers()  
		- reportMatch(winner, loser)  
			Note: Rematches are not allowed.  
		- deleteMatches()  
		- playerStandings()  
		- swissPairings()  
			Note: Byes implemented, but the same player may receive multiple byes.  
	tournament.sql: SQL database and table definitions  
		- Draws and multi-tournament database have fields and tables, but  
		-the corresponding API to use them have not been implemented.  

Usage steps:  

	
	If not installed, install Vagrant and VirtualBox.
	
	Clone the git repo containing project files.
		git clone https://github.com/Tyrfang/udacity-fullstack.git
	
	Clone the git repo containing vagrant setup and files
		git clone https://github.com/udacity/fullstack-nanodegree-vm.git
	
	Copy the vagrant folder in this directory into the vagrant folder provided by the Udacity course files
		cp -rf ./udacity-fullstack/project2-tournament_results/vagrant/ fullstack-nanodegree-vm/
	
	Navigate to the fullstack-nanodegree-vm/vagrant/
		cd fullstack-nanodegree-vm/vagrant
		
	Start up the viritual machine using Vagrant
		vagrant up
	
	Connect to the virtual machine using Vagrant
		vagrant ssh
	
	Navigate to the sync directory, and then the tournament directory
		cd /vagrant
		cd tournament
	
	Run PSQL to setup the initial database
		psql
			\i tournament.sql
			\q
	
	Execute any code that requires the given API.
		e.g.: python tournament_test.py
		
