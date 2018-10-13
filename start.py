#!/usr/bin/env python3

import subprocess
import threading
import time
import signal
import sys
import socket
import netifaces


shutting_down = 0

RUMPRUN="../rumprun/rumprun/bin/rumprun"
UNIKERNEL_PATH="./unikernels"

netifaces.ifaddresses('xenbr0')
IP_ADDRESS = netifaces.ifaddresses('xenbr0')[netifaces.AF_INET][0]['addr']

HOST=''
PORT=8080


def signal_handler( sig, frame ):
    global shutting_down
    shutting_down = 1


class UniKernel:    
  
    def __init__( self, name, ipaddress ):
        self.name = name
        self.ipaddress = ipaddress
        self.processorPercent = "0"
        self.startKernel()
        self.status = True
        self.timestamp = time.time()

    def getName( self ):
        return self.name

    def setProcessorPercent( self, percent ):
        self.processorPercent = percent

    def getProcessorPercent( self ):
        return self.processorPercent

    def setHeartbeat( self ):
        self.timestamp = time.time()

    def getHeartbeat( self ):
        return self.timestamp

    def startKernel( self ):
        cmd = RUMPRUN + " -S xen -d -M 16 -N " + self.name + \
              " -I xen0,xenif" + \
              " -W xen0,inet,static," + self.ipaddress + "/24 " + \
              UNIKERNEL_PATH + "/crash_kernel.run"
        print( cmd )
        
        p = subprocess.run( cmd.split() )

#        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        s.bind( ( HOST, PORT ) )
#        s.listen(1)
#        conn, addr = s.accept()
#        self.ipaddr = addr[0]
#        print( self.ipaddr )

    def endKernel( self ):
        cmd = "sudo xl destroy " + self.name
        p = subprocess.run( cmd.split() )
        

        

domains = [
    UniKernel("crash_kernel1", "192.168.1.134"),
#    UniKernel("crash_kernel2", "192.168.1.135"),
#    UniKernel("spin_kernel1", "192.168.1.136"),
#    UniKernel("spin_kernel2", "192.168.1.137")
]


def vm_monitor():

    global domain
    
    p = subprocess.Popen(['xentop', '-b', '-f', '-d 1'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.DEVNULL)
    
    while p.poll() is None and shutting_down is 0:
        
        line = p.stdout.readline().decode("utf-8")
        line = line.strip()
        
        if line is "":
            break

        if line.startswith("NAME"):
            continue
        
        for domain in domains:
            if domain.getName() in line:
                domain.setProcessorPercent( line.split()[3] )
                if float( domain.getProcessorPercent() ) < 90:
                    domain.setHeartbeat()
        
        
        

signal.signal( signal.SIGINT, signal_handler )
                
#    start the xentop thread and verify the global values get updated
monitor_thread = threading.Thread( target=vm_monitor, name="monitor_thread" )
monitor_thread.start()


while shutting_down is 0:
    for domain in domains:
        print( domain.getName() + " " + str( domain.getHeartbeat() ) )

    time.sleep(1)

#shutdown
for domain in domains:
    domain.endKernel()


monitor_thread.join()

