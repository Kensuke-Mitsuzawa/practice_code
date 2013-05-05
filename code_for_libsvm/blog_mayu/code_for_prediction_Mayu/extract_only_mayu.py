#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys,re,string

def clean(only_mayu):
    mayu_list = []
    for one_para in only_mayu:
        new_one_line = []
        for one_line in one_para:
            one_line = re.sub(r"(SUB-\d*:)|(MAIN-\d*:)","",one_line)
            one_line = one_line.strip("\n").strip()
            new_one_line.append(one_line)
            
        mayu_list.append(new_one_line)

    while mayu_list.count([]):
        mayu_list.remove([])

    return mayu_list

def only_mayu_(para_set):
    only_mayu = []

    for one_para in para_set:
        for one_line in one_para:
            if not re.findall(r"まゆゆより",one_line) == []:
                only_mayu.append(one_para)

    return only_mayu
        

def one_pattern(inputf):
    para_check = "no"
    para_set = []
    for line in inputf:
        if not re.findall(r"PATTERN:",line) == [] and para_check == "no":
            para_check = "yes"
            one_para = []
            continue

        
        if not re.findall(r"!MATCHED",line) == [] and para_check == "yes":
            para_check = "no"
            para_set.append(one_para)
            continue

        if para_check == "yes":
            one_para.append(line)

    return para_set
            

def extract():
    """
    This function reads result file of Webstemmer. 
    And this function extracts only the blog article of Mayuyu.
    
    After extraction,this function makes text clean(takes away any html tags)
    output is standard output. Use ">" in unix command.
    """
    out = open('mayu.txt','w')
    inputf = open('text.txt','r').readlines()
    
    para_set = one_pattern(inputf)
    only_mayu = only_mayu_(para_set)

    only_mayu = clean(only_mayu)
    
    count = 0
    yacount = 0
    ya_check = 'no'
    result_list = []
    

    for one in only_mayu:
        ya_check = "no"
        file_name = "./each_art/mayu" + "_" + str(count)
        each_file = open(file_name,'w')

        one_art_list = []
        for sent in one:

            if not re.findall("やびゃあ",sent) == []:
                ya_check = "yes"
                
            one_art_list.append(sent)
        
        sent_one_art = " ".join(one_art_list)
        if ya_check == "yes":
            file_name_ya = "./each_art/mayu" + "_" + "ya" + str(yacount)
            ya_file = open(file_name_ya,'w')
            ya_file.write(sent_one_art)
            ya_file.close()
            yacount = yacount + 1
       
        else:
            each_file.write(sent_one_art)
            each_file.close()
            count = count + 1

        result_list.append(sent_one_art)
                

    result = "\n".join(result_list)
    #print result
    out.write(result)

    out.close()

if __name__ == '__main__':
    extract()
