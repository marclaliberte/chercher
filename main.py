#!/usr/bin/python

import sys,csv,threading,ConfigParser,chercherConn,chercherDb,Queue,threading

q_in = Queue.Queue(maxsize=0)
num_worker_threads = 24


def worker():
    destPort = 443
    conn = chercherConn.chercherConn()
    while True:
        do = q_in.get()
        conn.testHost(do[0],do[1],do[2],destPort)
        q_in.task_done()

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

            for i in range(num_worker_threads):
                t = threading.Thread(target=worker)
                t.daemon = True
                t.start()

            for rank,host in reader:
                # For each line containing siteRank and Host
                # Add to threading queue for testin
                do = []
                do.append(testId)
                do.append(rank)
                do.append(host)
                q_in.put(do)

            q_in.join()
            print "Complete"
#                conn.testHost(testId,rank,host,destPort)


if __name__ == "__main__":
    # File called directly, run script
    # Grab CSV file from config
    config = ConfigParser.RawConfigParser()
    config.read("chercher.conf")
    csv_path = config.get('chercher', 'list_location')
    with open(csv_path, "rb") as f_obj:
        startScan(f_obj)
