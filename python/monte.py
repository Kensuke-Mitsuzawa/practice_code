#! /usr/bin/python
# -*- coding:utf-8 -*-
'''
Implementation of pi calculation using MonteCorlo Algorithm
http://nigohiroki.hatenablog.com/entry/2012/09/18/232306
'''
import math,random,sys

def pi(n):
    return float(monte(n))/(n/4)

def monte(n):
    count=0
    for i in range(1,n):
        if math.sqrt(pow(random.random(),2) + pow(random.random(),2)) < 1:
            count+=1
            continue
        else: pass

    return count

if __name__ == '__main__':
    print pi(int(sys.argv[1]))
                     
