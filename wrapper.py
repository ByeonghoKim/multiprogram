#!/usr/bin/python

import ctypes
from optparse import OptionParser
from subprocess import Popen
from multiprocessing import Process, Pool
from time import sleep
from string import atoi
from signal import SIGTERM
import os

# get stream ctypes

numa = ctypes.cdll.LoadLibrary('./numa.so')

# get command

def getcmd(cmd_list, script):
    try:
        scr = open(script)
    except IOError:
        print "cannot open", script
    lines = scr.readlines()
    for line in lines:
        line = line[:-1]
        line = line.split(' ')
        cmd_list.append(line)
    scr.close()
    return cmd_list

# start process

def start_proc(linelist, core, mem):
    print 'pid =', os.getpid()
    a = numa.core_mem_binding(core,
                              mem,
                              os.getpid())
    if a != 1:
        print 'Core, Memory Binding Failed to', os.getpid()
    os.execv(linelist[0],
             linelist)

# main

# argument parsing

usage = 'usage: %prog [options]'
parser = OptionParser(usage=usage)
parser.add_option('-s', '--script',
                  action='store', type='string', default='/dev/null',
                  dest='script', help='cmd list file')

(options,args) = parser.parse_args()

# initialize

cmd_list = list()
active_proc_list = list()

# get command from file

cmd_list = getcmd(cmd_list, options.script)

# Multiprocess not multithread

for cmd in cmd_list:
    proc = Process(target=start_proc, 
                   args=(cmd[2:], 
                         atoi(cmd[0]), 
                         atoi(cmd[1]),))
    active_proc_list.append([cmd, 
                             proc, 
                             False,
                             1])

# start process

for wait_process in active_proc_list:
    wait_process[1].start()

# polling

while True:
    try:
        for process in active_proc_list:
            if process[1].is_alive() != True:
                process[2] = True;
                proc = Process(target=start_proc,
                               args=(process[0][2:], 
                                     atoi(process[0][0]), 
                                     atoi(process[0][1]),))
                proc.start()
                process[1] = proc
                process[3] = process[3]+1
                print '=========='
                print process 
    
        end = True 
        for process in active_proc_list:
            if process[2] == False:
                end = False
            else:
                continue
    
        if end == True:
            for process in active_proc_list:
                os.kill(process[1].pid, SIGTERM)
            break
            
        sleep(0.2)
#        for process in active_proc_list:
#            print active_proc_list.index(process), process[2]
    except KeyboardInterrupt:
        os.killpg(os.getpgrp(), 9)
        for process in active_proc_list:
            print "Process [pid =", process[1].pid, "] killed"
            os.kill(process[1].pid, 9)
        sys.exit()

print "process ends"
