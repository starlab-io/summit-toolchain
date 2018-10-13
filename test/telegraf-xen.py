#!/usr/bin/env python3

import subprocess




class XenDom:    
  
    def __init__( self, name, id, status ):
        self.name = name
        self.status = status




def xentop_update_globals():

    p = subprocess.Popen(['xentop', '-b', '-f', '-d 1','-i2'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.DEVNULL)
    
    while p.poll() is None:
        
        line = p.stdout.readline().decode("utf-8")
        
        if line is "":
            break

        if line.strip().startswith("NAME"):
            continue
        
        domain = line.split()
       
        print( "domain:" + domain[0] + "cpu: " + domain[3] )
        


domains = {
    "crash-kern1":"",
    "crash-kern2":"",
    "spin-kern1":"",
    "spin-kern2":""
}
    
   
#    for line in xentop:
#      domain = line.split()
#      print_influx_data(domain[0],'cpu_time','cpu_time=' + domain[2] + 'i')
#      print_influx_data(domain[0],'cpu','load=' + domain[3])
#      print_influx_data(domain[0],'cpu','load=' + domain[3])
#      print_influx_data(domain[0],'mem','kb=' + domain[4] + 'i')
#      print_influx_data(domain[0],'nettx','nettx=' + domain[10] + 'i')
#      print_influx_data(domain[0],'netrx','netrx=' + domain[11] + 'i')
#      print_influx_data(domain[0],'disk_rd','disk_rd=' + domain[14] + 'i')
#      print_influx_data(domain[0],'disk_wr','disk_wr=' + domain[15] + 'i')


xentop_lines=xentop_update_globals()


