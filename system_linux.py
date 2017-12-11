#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import re
import sys
import requests
from os.path import join, isdir
import tarfile
import shutil
from commands import getoutput

class DiskInfo():
    def __init__(self):
        pass                                              
        }   

    def _get_usage(self, path):
        if not isdir(path):
            return "0"
        return getoutput("du -smL %s" % path).split()[0]

    def _disk(self):
         df = [i.split() for i in getoutput("df -TmP").splitlines()]
         types = {j[1]: i for i, j in enumerate(df)}
         dev = df[types.get("overlay") or types.get("xfs") or types.get("ext4") or 1]
         return dict(zip(df[0], dev))
        
    def get_disk_status(self):
        result = getoutput("df -m | grep harddisk")
        print result.split()[1:2]
         
        keys = ["total", "used", "available", "percent"]                                                      
        if not result:                                                                                        
            return dict(zip(keys, ["0"] * 4))                                                                 
        return dict(zip(keys, result.split()[1: 5]))                                                          

    def getcpu(self):                                                                        
        res={'usage':0,'corenum':0}
        def readcpuinfo():                                                               
            for line in open('/proc/stat'):                                              
                line = line.lstrip()                                                     
                counters = line.split()                                                  
                if len(counters) < 5:                                                    
                    continue                                                             
                if counters[0].startswith('cpu'):                                        
                    break                                                                
            total = 0                                                                    
            for i in xrange(1, len(counters)):                                           
                total = total + long(counters[i])                                        
                idle = long(counters[4])                                                 
            return {'total': total, 'idle': idle}                                        
                                                                                     
        counters1 = readcpuinfo()                                                        
        time.sleep(0.1)                                                                  
        counters2 = readcpuinfo()                                                        
        idle = counters2['idle'] - counters1['idle']                                     
        total = counters2['total'] - counters1['total']                                  
        res['usage']=str(100 - (idle * 100 / total))
        corenum=getoutput('cat /proc/cpuinfo |grep "processor"|wc -l')
        res['corenum']=corenum
        return res

    def getmemory(self):

        res = {'memtotal': 0, 'memfree': 0, 'buffers': 0, 'cached': 0}
        i = 0
        for line in open('/proc/meminfo'):
            if i == 4:
                break
            line = line.lstrip()
            memitem = [item.strip(":") for item in line.lower().split()]
            if memitem[0] in res:
                res[memitem[0]] = int(memitem[1])
                i = i + 1
                continue
        res["usage"]=str((res['memtotal'] - res['memfree'] ) * 100 / res["memtotal"])
        return res

