#-*- coding:utf-8 -*-

import sys, random

#イテレーション数は適当に
N=10
#タグ:確率を格納する辞書Yの定義とランダム値での初期化
Y={}
#あり得るタグをすべて格納するリスト
tag_set=[]
#タグ番号0から21まで設定する
for tag_number in range(0, 21):tag_set.append(tag_number)

def preprocess_Y(tag_set, Y, input_file_lines):
    token_list=[]
    for line in input_file_lines:
        map(lambda x: token_list.append(x.strip('/n').split()), input_file_lines)


    '''
    for y_i in tag_set:
        for y_i_minus_1 in tag_set:
            for y_i_plus_1 in tag_set:
            '''
            
def main():
    preprocess_Y(tag_set, Y, open('wiki-sample.word', 'r').readlines())

if __name__=='__main__':
    main()
