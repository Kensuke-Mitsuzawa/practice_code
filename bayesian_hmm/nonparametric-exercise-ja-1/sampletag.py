#! /usr/bin/python
# -*- coding:utf-8 -*-
__version__='2013/5/25'

def dirichlet_process(tag, y_i_minus_1_to_y_i, y_i_to_x_i, y_i_to_y_i_plus_1, p):
   pass 


def SampleTag(token_list, y_i, tag_set, Y):
    #確率を格納するリスト
    p=[]
    #いまのタグのカウントを−１する（グラム先生のスライドには削除って書いてあるけど，たぶん間違いだと思うんだ）
    for y_i_minus_or_plus_1 in tag_set:
        Y['y_i_minus_1_to_y_i'][str(y_i_minus_or_plus_1)+'_'+str(y_i)]-=1
        Y['y_i_to_y_i_plus_1'][str(y_i)+'_'+str(y_i_minus_or_plus_1)]-=1
    for x_i in token_list: Y['y_i_to_x_i'][str(y_i)+'_'+x_i]-=1
    #TODO diriclet-processの導出にはy_i, y_i-1のunigram頻度が必要．これも別に乱数（整数）で設定しておけばいいんだろうか？
    '''
    for tag in tag_set:
        p=dirichlet_process(tag, y_i_minus_1_to_y_i, y_i_to_x_i, y_i_to_y_i_plus_1, p)
    y_i=SampleOne(p)
    '''
