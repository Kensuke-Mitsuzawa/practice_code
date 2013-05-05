#! /usr/bin/python
# -*- coding:utf-8 -*-

import extract_only_mayu,mecab_morp

if __name__ == '__main__':
    extract_only_mayu.extract()
    mecab_morp.call_mecab()
    
    
