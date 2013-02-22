#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
scrip which extracts only raw texts from English Gigawords

usage:
re-write the parameter in if __name__ == "__main__"

in_n = input file name
out_n = out put file name
You can point the directry by rewriting dir_n

2013/2/22
"""


import sys,re,string,os

def get_raw(in_n,out_n):


    input = open(in_n,'r')
    out_f = open(out_n,'w')

    lines = input.readlines()

    one_paragraph = []
    para_flag = "off"
    for line in lines:
        if line == "<P>\n":
            para_flag = "on"
            continue
        
        if line == "</P>\n":
            para_flag = "off"
            for w_line in one_paragraph:
                out_f.write(w_line)

            one_paragraph = []
            continue

        if para_flag == "on":
            one_paragraph.append(line)
            continue

    out_f.close()

if __name__ == '__main__':

    in_n = "ltw.txt"
    dir_n = "/nwork/kensuke-mi/extract_raw_giga/raw_text/"
    out_n = dir_n +  "ltw.raw"
    
    get_raw(in_n,out_n)

    in_n = "nyt.txt"
    out_n = dir_n + "nyt.raw"

    get_raw(in_n,out_n)

    in_n = "unzip_cna.txt"
    out_n = dir_n + "cna.raw"

    get_raw(in_n,out_n)

    in_n = "wpb.txt"
    out_n = dir_n + "wpb.raw"

    get_raw(in_n,out_n)

    
    
