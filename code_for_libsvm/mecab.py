#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import MeCab
mecab = MeCab.Tagger('-Ochasen')

allfile = './data/all.txt'
data = open( allfile ).read()
node = mecab.parseToNode( data )
phrases = node.next

while phrases:
    try:
        print node.surface + " ",
        node = node.next
    except AttributeError:
       break
