# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 15:11:02 2015

@author: maikholzhey
"""
# import needed packages
import serial
import os
import sys
from datetime import datetime
import matplotlib
matplotlib.use('Qt4Agg') #Qt4Agg
import pyqtgraph as pg
import matplotlib.pyplot as plt
from drawnow import drawnow

print "Program terminates by Keyboard Interrupt: Crtl + C"

# needed functions
def query_yes_no(question, default="yes") : 
    valid = { "yes": True, "y": True, "ye": True, "no": False, "n": False }
    if default is None:
        prompt = " [y/n] "
    elif default == "yes" :
        prompt = " [Y/n] "
    elif default == "no" :
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please type correctly: 'y' or 'n' ? \n")

def makeFig(): # making the plot
    if descr :
        ymin = float(min(A))- 10
        ymax = float(max(A))+ 10
        plt.ylim(ymin,ymax)
        plt.title('Incoming Data: Arduino Impedanzmessung')
        plt.grid(True)
        plt.ylabel('Amplitude')
        plt.xlabel('TimeWindow 1/6 s')
        plt.plot(A,label='Impedanz')
        plt.legend(loc='upper right')
    elif plperf :
        pwidget.setData(T,A)
    else:
        plt.plot(A)

print "Open new Folder for saving Data"
#create new unique path
path = '/home/maikholzhey/Documents/alog/' + str(datetime.now())
#create folder
os.mkdir(path, 0755)
#change to folder
os.chdir(path)

print "Initialize..."

print "Performance \n============"
print "simple plot \t 6.93 SPS"
print "annotated plot \t 6.08 SPS"
print "without plot \t 157.35 SPS\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \
 \n157.35 SPS = True Sampling Rate\n"
 
descr = False
plperf = False
# should plotting be enabled?
# performance 6.08 SPS
plotok = query_yes_no("Should incoming Data be plotted?", default="yes")
# performance 6.93 SPS
if plotok:
    plperf = query_yes_no("Do you prefer Quality over Performance?", default="no")
    if not plperf:
        descr = query_yes_no("Should the plot be annotated?", default="no")
        
# without plotting
# perfomance 157.35 SPS - is true sampling rate of arduino

T=[]
A=[]

ser = serial.Serial('/dev/ttyACM0',115200)


# 8 hours of measurement: size: 84.288 MB DATA
f=open('datafile.txt','a')
#save time stamp
t=open('time.txt','a')
startTime = datetime.now()
t.write('Started Logging:\t'+ str(startTime) + '\n')
t.close()

if plperf:
    pwidget =pg.PlotCurveItem()
else:
    plt.ion() # interactive mode to plot live data
    plt.figure() # open a figure
    plt.show(block=False)
    
cnt=0 # it counts things... number of elements

print "Start Logging"

try:
    while True :
        while (ser.inWaiting()==0):
            pass
        try:
            data=ser.readline() # read data
            dataArray = data.split('\t')
            tmpT = float( dataArray[0])
            tmpA = float( dataArray[1])
            T.append(tmpT)
            A.append(tmpA)
            
            if plotok :
                drawnow(makeFig,show_once=True)
                plt.pause(.00001) # keeps drawnow from crashing
    
            cnt += 1 # important until plot buffer is filled up
            # safe data      
            f.write(data) # write to file
            f.close()
            f=open('datafile.txt','a')
            # keep plot vector tidy
            if(cnt>20):
                T.pop(0)
                A.pop(0)
        except KeyboardInterrupt:
            raise
        except:
            pass
except KeyboardInterrupt:
    pass
    
# save Time  
print "Save Stop Time"
t=open('time.txt','a')
stopTime = datetime.now()
duration = stopTime - startTime
t.write('Stopped Logging:\t'+ str(stopTime) + '\n')
t.write('Time passed:\t\t'+ str(duration) + '\n')
t.close()

#close plot Window
plt.close("all")
print "Logging Terminated"
