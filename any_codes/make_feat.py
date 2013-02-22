#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
This script prints the format for training libsvm.
The label for Noun singular is 0 and for Noun plural is 1.

Input:tagged text file. tag must be concatenated with underline"_". ex: car_NNN. The wall street journal tagset is used. If you use other tagset, please rewrite if condition in function feat.
output: standard output

If you want change input file, please rewrite input_f in function prepare_dic.
"""

def prepare_dic():
    """
    This function opens tagged file and constructs hash-map-dictionary(word - to - wordid)
    """
    
    hash_dic = {}
    
    input_f = open('tagged.txt','r').readlines()

    feat_count = 0
    for line in input_f:
        for each_w in line.split():

            word = (each_w.split("_"))[0]

            if word in hash_dic:
                pass
            
            if not word in hash_dic:

                hash_dic.setdefault(word,feat_count)

                feat_count = feat_count + 1

    feat(hash_dic,input_f)

def make_format(s_p,line_split,i,hash_dic):
    """
    This function makes format for libsvm.
    If condition is found(condition:tag is singular or plural), this function looks up 3 preceeding words and find id for each word. Finally,this functions prints "label id:1 ....". 
    """

    cand_list = []
                
    try:
        cand_list.append( (line_split[i-3].split("_"))[0] )
        cand_list.append( (line_split[i-2].split("_"))[0] )
        cand_list.append( (line_split[i-1].split("_"))[0] )
        cand_list.append( (line_split[i].split("_"))[0] )

    except IndexError:
        try:
            cand_list.append( (line_split[i-2].split("_"))[0] )
            cand_list.append( (line_split[i-1].split("_"))[0] )
            cand_list.append( (line_split[i].split("_"))[0] )
        
        except IndexError:
            try:
                cand_list.append( (line_split[i-1].split("_"))[0] )
                cand_list.append( (line_split[i].split("_"))[0] )

            except IndexError:
                pass


    print_list = []
    # 0 is label for singular
    if s_p == "s":
        label = "0"
    #i is label for plural
    if s_p == "p":
        label = "1"

    print_list.append(label)
    for e_word in cand_list:
                
        f_id = hash_dic[e_word]
        format = str(f_id) + ":" + str(1)
        print_list.append(format)
    print " ".join(print_list)
                    


def feat(hash_dic,input_f):
    """
    This function checks whether the tag for words is singular of plural.
    And calls function "make format".
    """
    for line in input_f:
        
        line_split = line.split()
        for i in range(len(line_split)):
        
            cand_list = []
            
            i_w_tag = (line_split[i].split("_"))[1]
            
        
            if i_w_tag == "NN" or i_w_tag == "NNP":
                s_p = "s"
                make_format(s_p,line_split,i,hash_dic)

            if i_w_tag == "NNNP" or i_w_tag == "NNS":
                s_p = "p"
                make_format(s_p,line_split,i,hash_dic)
        
if __name__ == '__main__':
    prepare_dic()
