#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import MeCab
mecab = MeCab.Tagger('-Ochasen')
names = { 'homura' : 1,
          'kyoko' : 2,
          'kyube' : 3,
          'madoka' : 4,
          'mami' : 5,
          'sayaka' : 6 }

allfile = './data/all.txt'
data = open( allfile ).read()
node = mecab.parseToNode( data )
words = {}
num = 0;
phrases = node.next
while phrases:
    try:
        k = node.surface
        k = k.strip().rstrip()
        if k in words:
            pass
        else:
            words[k] = num;
            num = num + 1 
        node = node.next
    except AttributeError:
       break

for i in names.keys():
    file = './data/' + i + '.txt'
    for line in open( file, 'r' ):
        line = line.strip().rstrip()
        n = mecab.parseToNode( line )
        p = n.next
        attrs = {}
        while p:
            try:
                k = n.surface
                if k not in words:
                   break 
                id = words[k]
                if id in attrs:
                    attrs[id] = attrs[id] + 1
                else:
                    attrs[id] = 1
                n = n.next
            except AttributeError:
               break

        print names[i],
        for ak in sorted( attrs.keys() ):
            print str(ak) + ":" + str(attrs[ak]), 
        print 
