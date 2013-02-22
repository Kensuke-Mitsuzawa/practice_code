#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,re,urllib,urllib2
urls = { 'http://www22.atwiki.jp/madoka-magica/pages/131.html' : 'madoka.txt', 
         'http://www22.atwiki.jp/madoka-magica/pages/57.html'  : 'homura.txt',
         'http://www22.atwiki.jp/madoka-magica/pages/123.html' : 'sayaka.txt',
         'http://www22.atwiki.jp/madoka-magica/pages/130.html' : 'mami.txt',
         'http://www22.atwiki.jp/madoka-magica/pages/132.html' : 'kyoko.txt',
         'http://www22.atwiki.jp/madoka-magica/pages/56.html'  : 'kyube.txt'
        }
opener = urllib2.build_opener()
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.51.22 (KHTML, like Gecko) Version/5.1.1 Safari/    534.51.22'
referer = 'http://www22.atwiki.jp/madoka-magica/'
opener.addheaders = [( 'User-Agent', ua ),( 'Referer', referer )]
for k,v in urls.iteritems():
    f = open( './data/' + v , 'w' )
    content = opener.open( k ).read()
    if re.compile( r'^「(.*?)」$', re.M ).search( content ) is not None: 
        lines = re.compile( r'^「(.*?)」$', re.M ).findall( content )
        for line in lines:
            f.write( line + "\n" )
f.close()
