#!/usr/bin/python
##
# chercherConn.py
# Tests and records supported protocol versions
##

import socket,ssl,sys,threading,time,chercherDb

class chercherThread(threading.Thread):
    def __init__(self,host,port,proto,cipher):
        super(chercherThread, self).__init__()
        self.host = host
        self.port = port
        self.proto = proto
        self.cipher = cipher

    def run(self):
        test = chercherConn()
        self.version,self.suite,self.error = test.testConnect(self.host,self.port,self.proto,self.cipher)


class chercherConn:
    def testHost(self,testId,rank,host,destPort):
        # Define required variables
        self.testId = testId
        self.rank = rank
        self.host = host
        self.destPort = destPort
        protocol0 = 'SSLv3'
        protocol1 = 'TLSv1'
        protocol2 = 'TLSv1_1'
        protocol3 = 'TLSv1_2'
        ciphers = ''

        # Open database connection
        db = chercherDb.chercherDb()
        conn = chercherConn()

        # Spawn threads
        thread1 = chercherThread(host,destPort,protocol0,ciphers)
        thread2 = chercherThread(host,destPort,protocol1,ciphers)
        thread3 = chercherThread(host,destPort,protocol2,ciphers)
        thread4 = chercherThread(host,destPort,protocol3,ciphers)

        # Start threads
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
        addToTaberror = db.addSiteResult(testId,rank,host,addr,destPort,ssl3v,str(ssl3c[0]),ssl3e,tls1v,str(tls1c[0]),tls1e,tls1_1v,str(tls1_1c[0]),tls1_1e,tls1_2v,str(tls1_2c[0]),tls1_2e)

        # Print results to prove it works
        print "***ADDED TO TABLE***"
        print "%s %s SSLv3: %s %s %s" % (rank,host,ssl3v,ssl3c[0],ssl3e)
        print "%s %s TLSv1: %s %s %s" % (rank,host,tls1v,tls1c[0],tls1e)
        print "%s %s TLSv1.1: %s %s %s" % (rank,host,tls1_1v,tls1_1c[0],tls1_1e)
        print "%s %s TLSv1.2: %s %s %s" % (rank,host,tls1_2v,tls1_2c[0],tls1_2e)

        # Update table with end time
        addEndTestErr = db.addTestEnd(testId)

    def testConnect(self,destName,destPort,proto,ciphers):
        # Define blank variables
        version = ""
        cipher = [""]
        error = ""
        protoList = "SSLv3 TLSv1 TLSv1.1 TLSv1.2"

        # Default ciphers to ALL
        if ciphers == '':
            ciphers = 'ALL'

        # Set up TLS socket context
        if proto == "SSLv3":
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
        elif proto == "TLSv1":
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        elif proto == "TLSv1_1":
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
        elif proto == "TLSv1_2":
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

        context.verify_mode = ssl.CERT_REQUIRED
        context.set_ciphers(ciphers)
        context.check_hostname = True
        context.load_default_certs()

        # Bind context to socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        ssl_sock = context.wrap_socket(s, server_hostname=destName)

        # Connect to dest
        try:
            ssl_sock.connect((destName, destPort))
            # Connection success
            version = ssl_sock.version()
            cipher = ssl_sock.cipher()

        except socket.error, msg:
            # Connection failed
            error = self.conErrorHandler(str(msg))

        except ssl.SSLError, msg:
            # SSL failed
            error = self.conErrorHandler(str(msg))

        except ssl.CertificateError, msg:
            error = "Certificate Error"
        except ValueError, msg:
            error = self.conErrorHandler(str(msg))

        if "Certificate Error" in error:
            # Certificate error, test without cert verify
            # Close old socket
            ssl_sock.close()

            # Build new socket
            if proto == "SSLv3":
                context1 = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
            elif proto == "TLSv1":
                context1 = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            elif proto == "TLSv1_1":
                context1 = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
            elif proto == "TLSv1_2":
                context1 = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

            context1.verify_mode = ssl.CERT_NONE
            context1.set_ciphers(ciphers)
            s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s1.settimeout(1)
            ssl_sock1 = context1.wrap_socket(s1, server_hostname=destName)

            # Connect to dest
            try:
                ssl_sock1.connect((destName, destPort))
                # Connection Success
                version = ssl_sock1.version()
                cipher = ssl_sock1.cipher()

            except socket.error, msg:
                error = self.conErrorHandler(str(msg))

            except ssl.SSLError, msg:
                error = self.conErrorHandler(str(msg))

            except ssl.CertificateError, msg:
                error = "Certificate Error"
            except ValueError, msg:
                error = self.conErrorHandler(str(msg))

        if version:
            versionBool = '1'
        else:
            versionBool = '0'


        return (versionBool,cipher,error)

    def conErrorHandler(self,errIn):
        # Take verbose error message and return easily saved error
        errOut = ''

        if "timed out" in errIn:
            # TCP connection timed out
            errOut = "Connection Timed Out"
        elif "Errno 111" in errIn:
            # Connection was refused by server
            errOut = "Connection Refused"
        elif "Errno -2" in errIn:
            # Name resulution error
            errOut = "Name Resolution Error"
        elif "Errno 104" in errIn:
            # Connection was reset
            errOut = "Connection Reset By Server"
        elif "WRONG_VERSION_NUMBER" in errIn:
            # SSL Wrong Version Number Alert
            errOut = "SSL Alert: Wrong Version Number"
        elif "SSLV3_ALERT_HANDSHAKE_FAILURE" in errIn:
            # SSLv3 Alert Handshake Failure
            errOut = "SSLv3 Alert: Handshake Failure"
        elif "TLSV1_ALERT_PROTOCOL_VERSION" in errIn:
            errOut = "TLSv1 Alert: Protocol Version"
        elif "CERTIFICATE_VERIFY_FAILED" in errIn:
            # Certificate Verification Failed
            errOut = "Certificate Error"
        elif "TLSV1_UNRECOGNIZED_NAME" in errIn:
            errOut = "TLSv1 Alert: Unrecognized Name"
        elif "EOF occurred in violation of protocol" in errIn:
            errOut = "Connection Closed Early"
        elif "empty or no certificate" in errIn:
            errOut = "Certificate Error"
        else:
            errOut = errIn

        return errOut

    def resolveName(self,host):
        # Resolve hostname and return address
	address = ''
        error = ''

        try:
            address = socket.gethostbyname(host)
        except socket.error, msg:
            error = self.conErrorHandler(str(msg))

        return (address,error)

