#!/usr/bin/python
##
# chercherConn.py
# Tests and records supported protocol versions
##

import socket,ssl,sys,threading,time

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
    def echoMarc(self,host,port,proto,cipher):
        version = "1"
        suite = ["AES-256","test1","128"]
        error = ""
        return version,suite,error

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
        elif "CERTIFICATE_VERIFY_FAILED" in errIn:
            # Certificate Verification Failed
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

