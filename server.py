# server program
import socket
import sys

HOST = ''     # IP
#HOST = '127.0.0.1'
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(100)
conn, addr = s.accept()
print 'Connected by', addr

try:
    while 1:
        data = conn.recv(1024)
        c = data.find('#')
        print "RCV: "+data
        if c >= 0:
            data = conn.recv(1024)
            while c >= 0:         
                c = data.find('#')
                print "RCV: "+data 
                if c >= 0:
                    data = conn.recv(1024)
                
        data = raw_input('MSG: ')
        c = data.find('#')
        conn.sendall(data)
        if c >= 0:
            while c >= 0:
                data = raw_input('MSG: ')
                c = data.find('#')
                conn.sendall(data)
                
except KeyboardInterrupt:       
    print "\n \n Connection Terminated \n"
    conn.close()
    sys.exit(0)
except socket.error:
    print "\n \n Connection Terminated \n"
    conn.close()
    sys.exit(0)
except:
    raise