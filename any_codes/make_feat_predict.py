#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
This script prints the format for training libsvm.
The label for Noun singular is 1 and for Noun plural is 2.

Input:tagged text file. tag must be concatenated with underline"_". ex: car_NNN. The wall street journal tagset is used. If you use other tagset, please rewrite if condition in function feat.
output: standard output

If you want change input file, please rewrite input_f in function prepare_dic.
"""

import sys,re,subprocess
from nltk.tag.stanford import POSTagger
from liblinear import *

def load_map_dic():

    map_dic = {}
    map_file = open('map_dic.tsv','r')
    lines = map_file.readlines()

    for line in lines:
        line = line.strip("\n")
        tmp_list = line.split("\t")

        if not tmp_list[0] in map_dic:
            map_dic.setdefault(tmp_list[0],tmp_list[1])

        else:
            pass

    return map_dic

def stan_pos(input_sent):
    """
    This function calls stanford POS tagger.In this function Stanford POS tagger directory must be in the same directory.And this function chooses model "wsj left 3 words" as normal POS tagging model. If  you want to use other POS tagging models, please change first argument of st = POSTagger() below.

    """
    eval_sent = []

    st = POSTagger("./stanford-postagger-2012-11-11/models/wsj-0-18-left3words.tagger","./stanford-postagger-2012-11-11/stanford-postagger.jar")

    pos_result = st.tag(input_sent.split())
    for one_tuple in pos_result:
        pos_format = one_tuple[0] + "_" + one_tuple[1]
        
        eval_sent.append(pos_format)

    eval_sent = reg_form(eval_sent)
    return eval_sent


def reg_form(eval_sent):
    """
    This function regularizes anyword form.
    I defined (word). or (word), and word_POS$ as pattern. If you want to find more patterns, add pattern below
    """
    for i in range(len(eval_sent)):
        if not re.findall(r'($|\.|,)_',eval_sent[i]) == []:
            eval_sent[i] = re.sub(r'($|\.|,)','',eval_sent[i])
        
        if not re.findall(r'_(\w)$',eval_sent[i]) == []:
            eval_sent[i] = re.sub(r'$','',eval_sent[i])


    return eval_sent

def get_file_name():
    
    argvs = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argvs) # 引数の個数


    if (argc != 2):   # 引数が足りない場合は、その旨を表示
        print 'Usage: # python %s filename' % argvs[0]
        quit()         # プログラムの終了
 

    file_name = argvs[1]
    
    return file_name


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
            if e_word in hash_dic:
                f_id = hash_dic[e_word]
                sort_list.append(int(f_id))
        
        #delete repetition elements
        sort_list = list(set(sort_list))
        # sort by order
        sort_list.sort()
    
        #print_list.append(label)
        for id in sort_list:
            format = str(id) + ":" + str(1)
            print_list.append(format)

        print " ".join(print_list)

        return print_list

def predict_label(print_list):
    assert isinstance(print_list, list)
    model_ = liblinear.load_model('./cna_feat.train.model')
    predict_dic = {}
    for feat in print_list:
        predict_dic.setdefault(int((feat.split(":"))[0]),1)

    #print predict_dic
    x0, max_idx = gen_feature_nodearray(predict_dic)
    label = liblinear.predict(model_, x0)
    
    return label



def test(hash_dic,eval_sent):
    """
    This function checks whether the tag for words is singular of plural.
    And calls function "make format".
    """

    print eval_sent

    i_w_tag = ""

    for i in range(len(eval_sent)):


        cand_list = []
        try:
            i_w_tag = (eval_sent[i].split("_"))[1]
        except IndexError:
            pass
        
        #label=1 is for s
        if i_w_tag == "NN" or i_w_tag == "NNP":
            s_p = "s"
            print_list = make_format(s_p,eval_sent,i,hash_dic)
            label = predict_label(print_list)
            #print label
            if label == 1.0:
                print "correct:",eval_sent[i],"\n"
            else:
                print "wrong!",eval_sent[i],"\n"

        #label=2 is for p
        if i_w_tag == "NNNP" or i_w_tag == "NNS":
            s_p = "p"
            print_list = make_format(s_p,eval_sent,i,hash_dic)
            label = predict_label(print_list)
            #print label
            if label == 2.0:
                print "correct:",eval_sent[i],"\n"

            else:
                print "wrong!",eval_sent[i],"\n"



        
if __name__ == '__main__':

    input_sent = raw_input("please type sentence.\n")
    #file_name = get_file_name()
    #input_sent = open(file_name,'r')
    eval_sent = stan_pos(input_sent)
    map_dic = load_map_dic()
    test(map_dic,eval_sent)




