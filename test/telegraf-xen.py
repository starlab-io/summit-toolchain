#
#Taken from: https://gist.github.com/ernetas/b14ad803162baf7d7635a8d8b31b8d64
#




#!/usr/bin/env python3
import socket
hostname = socket.gethostname()
import subprocess
import time

def print_influx_data(xendomain, item, value):
  global timestamp
  print('xen_' + item + ',domain=' + xendomain + ',host=' + hostname + ' ' + value + ' ' + timestamp)


def get_xentop_lines():
  # Using -i1 does not show correct CPU usage
  # Since collecting data is slow, we must run xentop only once and collect all the needed data from one run
  p = subprocess.Popen(['xentop', '-b', '-f', '-i2'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
  out, _ = p.communicate(timeout=60)
  out = out.decode('utf-8')
  # Ignore the first iteration, as data there is not correct (e.g. CPU usage 0%)
  # Start reading lines only after second line starting with 'NAME' (second iteration)
  iteration = 0
  
  xentop = []
   
  for line in out.splitlines():
    if iteration < 2 and line.strip().startswith('NAME'):
      iteration += 1
    elif iteration == 2 and not line.strip().startswith('NAME'):
      xentop.append(line.strip())
  

  for line in xentop:
    domain = line.split()
#    print_influx_data(domain[0],'cpu_time','cpu_time=' + domain[2] + 'i')
#    print_influx_data(domain[0],'cpu','load=' + domain[3])
    print_influx_data(domain[0],'cpu','load=' + domain[3])
#    print_influx_data(domain[0],'mem','kb=' + domain[4] + 'i')
#    print_influx_data(domain[0],'nettx','nettx=' + domain[10] + 'i')
#    print_influx_data(domain[0],'netrx','netrx=' + domain[11] + 'i')
#    print_influx_data(domain[0],'disk_rd','disk_rd=' + domain[14] + 'i')
#    print_influx_data(domain[0],'disk_wr','disk_wr=' + domain[15] + 'i')


timestamp = str("%.9f" % time.time()).replace('.', '') # A little bit more exact than doing this for each xentop line
xentop_lines=get_xentop_lines()


