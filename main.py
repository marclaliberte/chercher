#!/usr/bin/python

import sys,csv,chercherConn,chercherDb

# Define funciton to read CSV
def startScan(file_obj):
    # Define variables
    destPort = 443
    protocol0 = 'SSLv3'
    protocol1 = 'TLSv1'
    protocol2 = 'TLSv1_1'
    protocol3 = 'TLSv1_2'
    ciphers = ''

    # Prep chercher includes
    db = chercherDb.chercherDb()
    conn = chercherConn.chercherConn()

    # Add new test to database
    testId,addError = db.addTest()

    if not addError:
        # No error adding new test to database
        # Create resulte table
        addTabError = db.addResultTable(testId)

        if not addTabError:
            # No error creating result table
            # Begin test

                # Read csv file and test each host
                reader = csv.reader(file_obj)
                for rank,host in reader:
                    # test the host for SSL3
                    ssl3v,ssl3c,ssl3e = conn.testConnect(host,destPort,protocol0,ciphers)

                    # test the host for TLSv1
                    tls1v,tls1c,tls1e = conn.testConnect(host,destPort,protocol1,ciphers)

                    # test the host for TLSv1_1
                    tls1_1v,tls1_1c,tls1_1e = conn.testConnect(host,destPort,protocol2,ciphers)

                    # Test the host for TLSv1_2
                    tls1_2v,tls1_2c,tls1_2e = conn.testConnect(host,destPort,protocol3,ciphers)

	            # Resolve hostname
                    addr,dnserr = conn.resolveName(host)

                    # Add results to table

                    addToTaberror = db.addSiteResult(testId,host,addr,destPort,ssl3v,str(ssl3c[0]),ssl3e,tls1v,str(tls1c[0]),tls1e,tls1_1v,str(tls1_1c[0]),tls1_1e,tls1_2v,str(tls1_2c[0]),tls1_2e)

                    print "***ADDED TO TABLE***"
                    print "%s %s SSLv3: %s %s %s" % (rank,host,ssl3v,ssl3c[0],ssl3e)
                    print "%s %s TLSv1: %s %s %s" % (rank,host,tls1v,tls1c[0],tls1e)
                    print "%s %s TLSv1.1: %s %s %s" % (rank,host,tls1_1v,tls1_1c[0],tls1_1e)
                    print "%s %s TLSv1.2: %s %s %s" % (rank,host,tls1_2v,tls1_2c[0],tls1_2e)

                    # Update table with end time
                    addEndTestErr = db.addTestEnd(testId)

csv_path = "top-10.csv"
with open(csv_path, "rb") as f_obj:
    startScan(f_obj)

#destName = 'blogspot.com'
#destPort = 443
#protocol0 = 'SSLv3'
#protocol1 = 'TLSv1'
#protocol2 = 'TLSv1_1'
#protocol3 = 'TLSv1_2'
#ciphers = ''

#test = chercherConn.chercherConn()

#version0, cipher0, error0 = test.testConnect(destName,destPort,protocol0,ciphers)
#version1, cipher1, error1 = test.testConnect(destName,destPort,protocol1,ciphers)
#version2, cipher2, error2 = test.testConnect(destName,destPort,protocol2,ciphers)
#version3, cipher3, error3 = test.testConnect(destName,destPort,protocol3,ciphers)

#print "Host: ", destName, ":", destPort
#print "Test 1: ", version0, cipher0, error0
#print "Test 2: ", version1, cipher1, error1
#print "Test 3: ", version2, cipher2, error2
#print "Test 4: ", version3, cipher3, error3