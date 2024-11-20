import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)

class Scanner(object):
    def __init__(self):
        self.runner()

    def connScan(self):
        try:
            connSkt = socket(AF_INET, SOCK_STREAM)
            connSkt.connect((self.tgtHost, self.tgtPort))
            connSkt.send('Attack vector initialisation!!!\r\n')
            results = connSkt.recv(100)
            screenLock.acquire()
            print(f"[+]{self.tgtPort}/tcp open")
            print(f"[+] {str(results)}")
        except:
            screenLock.acquire()
            print("[-]{self.tgtPort}/tcp closed")
        finally:
            screenLock.release()
            connSkt.close()
    
    def portScan(self, tgtHost, tgtPorts):
        try:
            tgtIP = gethostbyname(self.tgtHost)
        except:
            print(f"[-] Cannot resolve '{self.tgtHost}': Unknown host")
            return
        
        try:
            tgtName = gethostbyaddr(tgtIP)
            print(f"\n[+] Scan results for: {tgtName[0]}")
        except:
            print(f"\n[+] Scan results for: {tgtIP}")

        setdefaulttimeout(1)
        for self.tgtPort in self.tgtPorts:
            t = Thread(target=self.connScan, args=(self.tgtHost, int(self.tgtPort)))
            t.start()

    def runner(self):
        parser = optparse.OptionParser('usage%prog '+\
                                       '-H <target host> -p <target_port>')
        parser.add_option('-H', dest='self.tgtHost', type='string', \
                          help='specify target host')
        parser.add_option('-p', dest='self.tgtPort', type='string', \
                          help='specify target port[s] separated by comma')
        (options, args) = parser.parse_args()
        self.tgtHost = options.tgtHost
        self.tgtPorts = str(options.tgtPort).split(',')
        if (self.tgtHost == None) | (self.tgtPorts[0] == None):
            print(parser.usage)
            exit(0)
        self.portScan(self.tgtHost, self.tgtPorts)


if __name__ == '__main__':
    s = Scanner()

