#!/usr/bin/python
##
# chercherConfig.py
# Handles creating and editing the script config file
##

import ConfigParser,getpass

class chercherConfig:
    def createConfig(self):
        # Populate new configuration file

        # Create config object
        config = ConfigParser.RawConfigParser()

        # Read current configuration
        config.read("chercher.conf")

        # Get current settings
        mysql_host = config.get('mysqldb','host')
        mysql_port = config.get('mysqldb','port')
        mysql_database = config.get('mysqldb','database')
        mysql_user = config.get('mysqldb','user')
        mysql_password = config.get('mysqldb','password')

        # Print out intro
        print "Chercher Configuration Setup"
        
        # Ask user for MySQL host

        # Ask user for MySQL database name
        i_mysql_database = raw_input('MySQL Database [%s]: ' % mysql_database)

        # Ask user for MySQL username
        i_mysql_user = raw_input('MySQL User [%s]: ' % mysql_user)

        # Ask user for MySQL Password
        i_mysql_password = getpass.getpass("MySQL Password: ")

        # Update config with user input
        config.set('mysqldb', 'database', i_mysql_database)
        config.set('mysqldb', 'user', i_mysql_user)
        config.set('mysqldb', 'password', i_mysql_password)

        # Save to configuration
        with open('chercher.conf', 'wb') as configfile:
            config.write(configfile)

if __name__ == "__main__":
    config = chercherConfig()
    config.createConfig()
