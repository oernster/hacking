import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)

class Scanner(object):
    def __init__(self):
        self.runner()

    def connScan(self, tgtHost, tgtPort):
        try:
            connSkt = socket(AF_INET, SOCK_STREAM)
            connSkt.connect((tgtHost, tgtPort))
            connSkt.send('Attack vector initialisation!!!\r\n')
            results = connSkt.recv(100)
            screenLock.acquire()
            print(f"[+]{tgtPort}/tcp open")
            print(f"[+] {str(results)}")
        except:
            screenLock.acquire()
            print("[-]{tgtPort}/tcp closed")
        finally:
            screenLock.release()
            connSkt.close()
    
    def portScan(self, tgtHost, tgtPorts):
        try:
            tgtIP = gethostbyname(tgtHost)
        except:
            print(f"[-] Cannot resolve '{tgtHost}': Unknown host")
            return
        
        try:
            tgtName = gethostbyaddr(tgtIP)
            print(f"\n[+] Scan results for: {tgtName[0]}")
        except:
            print(f"\n[+] Scan results for: {tgtIP}")

        setdefaulttimeout(1)
        for tgtPort in tgtPorts:
            t = Thread(target=self.connScan, args=(tgtHost, int(tgtPort)))
            t.start()

    def runner(self):
        parser = optparse.OptionParser('usage%prog '+\
                                       '-H <target host> -p <target_port>')
        parser.add_option('-H', dest='tgtHost', type='string', \
                          help='specify target host')
        parser.add_option('-p', dest='tgtPort', type='string', \
                          help='specify target port[s] separated by comma')
        (options, args) = parser.parse_args()
        tgtHost = options.tgtHost
        tgtPorts = str(options.tgtPort).split(',')
        if (tgtHost == None) | (tgtPorts[0] == None):
            print(parser.usage)
            exit(0)
        self.portScan(tgtHost, tgtPorts)


if __name__ == '__main__':
    s = Scanner()

