!/usr/bin/python

import sys,csv,chercherConn,chercherDb,threading

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
                    thread1 = chercherConn.chercherThread(host,destPort,protocol0,ciphers)

                    # test the host for TLSv1
                    thread2 = chercherConn.chercherThread(host,destPort,protocol1,ciphers)

                    # test the host for TLSv1_1
                    thread3 = chercherConn.chercherThread(host,destPort,protocol2,ciphers)

                    # Test the host for TLSv1_2
                    thread4 = chercherConn.chercherThread(host,destPort,protocol3,ciphers)

                    # Start Threads
                    thread1.start()
                    thread2.start()
                    thread3.start()
                    thread4.start()

                    # Wait for results
                    thread1.join()
                    thread2.join()
                    thread3.join()
                    thread4.join()

                    # Save results from each thread
                    ssl3v,ssl3c,ssl3e = thread1.version,thread1.suite,thread1.error
                    tls1v,tls1c,tls1e = thread2.version,thread2.suite,thread2.error
                    tls1_1v,tls1_1c,tls1_1e = thread3.version,thread3.suite,thread3.error
                    tls1_2v,tls1_2c,tls1_2e = thread4.version,thread4.suite,thread4.error

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

csv_path = "top-50k.csv"
with open(csv_path, "rb") asConn:
    startScan(f_obj)
