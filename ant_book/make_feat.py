#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
This script prints the format for training libsvm.
The label for Noun singular is 1 and for Noun plural is 2.

Input:tagged text file. tag must be concatenated with underline"_". ex: car_NNN. The wall street journal tagset is used. If you use other tagset, please rewrite if condition in function feat.
output: standard output

If you want change input file, please rewrite input_f in function prepare_dic.
"""

import sys
def get_file_name():
    
    argvs = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argvs) # 引数の個数
    # デバッグプリント
    print argvs
    print argc
    print
    if (argc != 2):   # 引数が足りない場合は、その旨を表示
        print 'Usage: # python %s filename' % argvs[0]
        quit()         # プログラムの終了
 
    print 'The content of %s ...n' % argvs[1]
    file_name = argvs[1]
    
    return file_name


def prepare_dic(file_name):
    """
    This function opens tagged file and constructs hash-map-dictionary(word - to - wordid)
    """
    
    hash_dic = {}
    
    input_f = open(file_name,'r').readlines()
    tsv_file = open('map_dic.tsv','w')

    feat_count = 1
    for line in input_f:
        for each_w in line.split():

            word = (each_w.split("_"))[0]

            if word in hash_dic:
                pass
            
            if not word in hash_dic:

                hash_dic.setdefault(word,feat_count)

                feat_count = feat_count + 1

    
    for each_key in hash_dic:
        value = hash_dic[each_key]
        tsv_format = str(each_key) + "\t" + str(value) + "\n"

        tsv_file.write(tsv_format)
        


    feat(hash_dic,input_f)

def make_format(s_p,line_split,i,hash_dic):
    """
    This function makes format for libsvm.
    If condition is found(condition:tag is singular or plural), this function looks up 3 preceeding words and find id for each word. Finally,this functions prints "label id:1 ....". 
    """

    cand_list = []

    if i-2 == 0 and i+3 < len(line_split)-1:

        cand_list.append( (line_split[i-2].split("_"))[0] )
        cand_list.append( (line_split[i-1].split("_"))[0] )
        
        cand_list.append( (line_split[i+3].split("_"))[0] )
        cand_list.append( (line_split[i+2].split("_"))[0] )
        cand_list.append( (line_split[i+1].split("_"))[0] )

    if i-1 == 0 and i+3 < len(line_split)-1:

        cand_list.append( (line_split[i-1].split("_"))[0] )
        
        cand_list.append( (line_split[i+3].split("_"))[0] )
        cand_list.append( (line_split[i+2].split("_"))[0] )
        cand_list.append( (line_split[i+1].split("_"))[0] )

    if i == 0 and i+3 < len(line_split)-1:

        cand_list.append( (line_split[i+3].split("_"))[0] )
        cand_list.append( (line_split[i+2].split("_"))[0] )
        cand_list.append( (line_split[i+1].split("_"))[0] )

    if i-3 >= 0 and i+2 == len(line_split)-1:

        cand_list.append( (line_split[i-3].split("_"))[0] )
        cand_list.append( (line_split[i-2].split("_"))[0] )
        cand_list.append( (line_split[i-1].split("_"))[0] )
        
        cand_list.append( (line_split[i+1].split("_"))[0] )
        cand_list.append( (line_split[i+2].split("_"))[0] )

    if i-3 >= 0 and i+1 == len(line_split)-1:

        cand_list.append( (line_split[i-3].split("_"))[0] )
        cand_list.append( (line_split[i-2].split("_"))[0] )
        cand_list.append( (line_split[i-1].split("_"))[0] )
        
        cand_list.append( (line_split[i+1].split("_"))[0] )


    if i-3 >= 0 and i == len(line_split)-1:

        cand_list.append( (line_split[i-3].split("_"))[0] )
        cand_list.append( (line_split[i-2].split("_"))[0] )
        cand_list.append( (line_split[i-1].split("_"))[0] )      
        

    #if i-3 has more than 0
    if i-3 >= 0 and i+3 <= len(line_split)-1:

        #対象の語が文頭から３単語以上の場合
        # look up 3 previous 3 words
        cand_list.append( (line_split[i-3].split("_"))[0] )
        cand_list.append( (line_split[i-2].split("_"))[0] )
        cand_list.append( (line_split[i-1].split("_"))[0] )
        #look up POS tag of word itself
        #cand_list.append( (line_split[i].split("_"))[1] )

        #対象の語が文末から３単語以上の場合
        cand_list.append( (line_split[i+3].split("_"))[0] )
        cand_list.append( (line_split[i+2].split("_"))[0] )
        cand_list.append( (line_split[i+1].split("_"))[0] )

    

    if not cand_list == []:

        sort_list = []
        print_list = []
        # 0 is label for singular
        if s_p == "s":
            label = "1"
        #i is label for plural
        if s_p == "p":
            label = "2"

        for e_word in cand_list:            
            f_id = hash_dic[e_word]
            sort_list.append(f_id)
        #delete repetition elements
        sort_list = list(set(sort_list))
        # sort by order
        sort_list.sort()
    
        print_list.append(label)
        for id in sort_list:
            format = str(id) + ":" + str(1)
            print_list.append(format)

        print " ".join(print_list)
                    


def feat(hash_dic,input_f):
    i_w_tag = ""

    """
    This function checks whether the tag for words is singular of plural.
    And calls function "make format".
    """
    for line in input_f:
        
        line_split = line.split()
        for i in range(len(line_split)):
        
            cand_list = []
            try:
                i_w_tag = (line_split[i].split("_"))[1]
            except IndexError:
                pass
        
            if i_w_tag == "NN" or i_w_tag == "NNP":
                s_p = "s"
                make_format(s_p,line_split,i,hash_dic)

            if i_w_tag == "NNNP" or i_w_tag == "NNS":
                s_p = "p"
                make_format(s_p,line_split,i,hash_dic)
        
if __name__ == '__main__':
    file_name = get_file_name()
    prepare_dic(file_name)
