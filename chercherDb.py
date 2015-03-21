#!/user/bin/python
##
# chercherDb.py
# Handles interaction with mysql
##

import sys,datetime,ConfigParser,MySQLdb

class chercherDb:

    # Retrieve MySQL settings from config
    config = ConfigParser.RawConfigParser()
    config.read("chercher.conf")

    dbHost = config.get('mysqldb','host')
    dbName = config.get('mysqldb','database')
    dbUser = config.get('mysqldb','user')
    dbPass = config.get('mysqldb','password')

    def addTest(self):
        # Connects to mysql, adds a new entryto the testTab table, returns test ID
        # Define variables
        testId = ''
        error = ''
        
        # Open database connection
        db = MySQLdb.connect(self.dbHost,self.dbUser,self.dbPass,self.dbName)

        # Prepare cursor object
        cur = db.cursor()

        # Save Timestamp
        dt = datetime.datetime.utcnow()

        # Prepare statement
        sql = "INSERT INTO testTab(startTime) VALUES('%s')" % dt

        # Attempt to execute command
        try:
            cur.execute(sql)
            db.commit()
            # Save row ID
            testId = cur.lastrowid
        except:
            db.rollback()

        # Close connection
        db.close()

        # Return results
        return (testId,error)

    def addTestEnd(self,testNum):
        # Connects to mysql, updates testNum in testTab with the end time
        # Define variables
        error = ''

        # Open database connection
        db = MySQLdb.connect(self.dbHost,self.dbUser,self.dbPass,self.dbName)

        # Prepare cursor object
        cur = db.cursor()

        # Save Timestamp
        dt = datetime.datetime.utcnow()

        # Prepare statement
        sql = "UPDATE testTab SET endTime = '%s' WHERE id = '%s'" % (dt,testNum)

        # Attempt to execute command
        try:
            cur.execute(sql)
            db.commit()
        except:
            db.rollback()

        # Close connection
        db.close()

        return (error)

    def addResultTable(self,testNum):
        # Create result table for test number
        # Define variables
        error = ''
        tabName = "result_" + str(testNum)

        # Open database connection
        db = MySQLdb.connect(self.dbHost,self.dbUser,self.dbPass,self.dbName)

        # Prepare cursor object
        cur = db.cursor()

        # Prepare statement
        sql = "CREATE TABLE %s (siteNum INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, scanTime DATETIME NOT NULL, host VARCHAR(128) NOT NULL, addr VARCHAR(40), port SMALLINT UNSIGNED NOT NULL DEFAULT '443', ssl3 BOOLEAN NOT NULL, ssl3C VARCHAR(64), ssl3E VARCHAR(64), tls1 BOOLEAN NOT NULL, tls1C VARCHAR(64), tls1E VARCHAR(64), tls1_1 BOOLEAN NOT NULL, tls1_1C VARCHAR(64), tls1_1E VARCHAR(64), tls1_2 BOOLEAN NOT NULL, tls1_2C VARCHAR(64), tls1_2E VARCHAR(64))" % tabName

        # Attempt to execute command
        try:
            cur.execute(sql)
            db.commit()
        except:
            db.rollback()

        # Close connection
        db.close()

        return (error)

    def addSiteResult(self,testNum,host,addr,port,ssl3,ssl3C,ssl3E,tls1,tls1C,tls1E,tls1_1,tls1_1C,tls1_1E,tls1_2,tls1_2C,tls1_2E):
        # Adds site data to table for testNum
        # Define variables
        error = ''
        tabName = "result_" + str(testNum)

        # Open database connection
        db = MySQLdb.connect(self.dbHost,self.dbUser,self.dbPass,self.dbName)

        # Prepare cursor object
        cur = db.cursor()

        # Save Timestamp
        dt = datetime.datetime.utcnow()

        # Prepare statement
        sql = "INSERT INTO %s (scanTime, host, addr, port, ssl3, ssl3C, ssl3E, tls1, tls1C, tls1E, tls1_1, tls1_1C, tls1_1E, tls1_2, tls1_2C, tls1_2E) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (tabName,dt,host,addr,port,ssl3,ssl3C,ssl3E,tls1,tls1C,tls1E,tls1_1,tls1_1C,tls1_1E,tls1_2,tls1_2C,tls1_2E)

        # Attempt to execute command
        try:
            cur.execute(sql)
            db.commit()
        except MySQLdb.Error, e:
            db.rollback()

        # Close connection
        db.close()

        return (error)

#test = chercherDb()
#test.addSiteResult('5','www.google.com','1.1.1.1','443','1','AES-256','','1','AES-256','','1','3DES','','0','','PROTO ERROR')
