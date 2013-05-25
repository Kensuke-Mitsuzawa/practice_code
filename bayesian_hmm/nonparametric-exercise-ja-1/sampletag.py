#! /usr/bin/python
# -*- coding:utf-8 -*-
__version__='2013/5/25'

def dirichlet_process(tag, y_i_minus_1_to_y_i, y_i_to_x_i, y_i_to_y_i_plus_1, p):
   pass 


def SampleTag(token_list, y_i, tag_set, Y):
    #確率を格納するリスト
    p=[]
    #いまのタグのカウントを初期化する
    for y_i_minus_or_plus_1 in tag_set:
        Y['y_i_minus_1_to_y_i'][str(y_i_minus_or_plus_1)+'_'+str(y_i)]==0
        Y['y_i_to_y_i_plus_1'][str(y_i)+'_'+str(y_i_minus_or_plus_1)]==0
    for x_i in token_list: Y['y_i_to_x_i'][str(y_i)+'_'+x_i]==0
    print Y['y_i_minus_1_to_y_i']
    '''
    for tag in tag_set:
        p=dirichlet_process(tag, y_i_minus_1_to_y_i, y_i_to_x_i, y_i_to_y_i_plus_1, p)
    y_i=SampleOne(p)
    '''
