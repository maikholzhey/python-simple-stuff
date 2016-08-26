# Echo client program
import socket
import sys

HOST = ''    # The remote host
#HOST = '127.0.0.1'  # loopback
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

try:
    while 1	:
        data = raw_input('MSG: ')
        c = data.find('#')
        s.sendall(data)
        if c >= 0:
            while c >= 0:
                data = raw_input('MSG: ')
                c = data.find('#')
                s.sendall(data)
                
        
        data = s.recv(1024)
        c = data.find('#')
        print "RCV: "+data
        if c >= 0:
            data = s.recv(1024)
            while c >= 0:         
                c = data.find('#')
                print "RCV: "+data
                if c > 0 :
                    data = s.recv(1024)
        
except KeyboardInterrupt:
    print "\n \n Connection Terminated \n"
    s.close()
    sys.exit(0)
except socket.error:
    print "\n \n Connection Terminated \n"
    s.close()
    sys.exit(0)
except:
    raise
	