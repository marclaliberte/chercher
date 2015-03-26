# Chercher
######(shair-shey)


### Description
Chercher is a set of Python scripts used to parse and test SSL/TLS
protocol support on the Alexa top 1-Million site list in CSV format.

### Required Applications
Python 2.7.9+, MySQL 5+, OpenSSL 1.0.1+

### Required Python Modules
- sys - Basic set of variables and functions
- datetime - Basic timestamp handling
- csv - Used to read the Alexa top 1-Million CSV file
- socket - Used by test client to connect to sites
- ssl - USed by test client to negotiate SSL/TLS
- threading - Used to allow multiple concurrent tests via threading
- Queue - Used to manage multiple threads
- MySQLdb - Used to interface with MySQL database

### Installation
1. Install required applications and Python modules.
2. Update chercher.conf with MySQL database and credentials

### Usage
1. Run main.py
2. Wait
