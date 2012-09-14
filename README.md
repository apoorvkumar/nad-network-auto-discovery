-------------------------------
Developed by:- 

Apoorva Kumar
Raj Kamal Singh
Amit Kumar Swami

-----------------------





-----------------------




nad-network-auto-discovery-
===========================

Auto discovery system for an SNMP enabled network without the whole of the system.


Instruction for using the code.
-------------------------------

Setting up the discovery procedure
----------------------------------
Copy the autodiscovery directory to the home folder.
Database credentials need to be given to the following files
getIpConfig.py
  line 203
	line 212	
	line 262


Setting up the front end
------------------------
Copy all files in the www folder to /var/www

Database configuration
Run the scripts ad1.sql and ad2.sql found in the sql directory
Database credentials need to be given to the following files in www
/var/www/autodiscovery/application/config/database.php
	provide the path of the dbconfig file which is located in the autodiscovery directory : line 54
	provide the db connection credentials : starting line 51
	
/var/www/topology.php : starting line 6
	provide the path of the dbconfig file which is located in the autodiscovery directory : line 9
	provide the db connection credentials : starting line 6

