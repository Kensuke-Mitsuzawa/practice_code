#-*- coding:utf-8 -*-

import sys, random
import sampletag

#イテレーション数は適当に
N=10
#y_i_-1からy_iの遷移の組み合わせを保存しておくリスト
y_i_minus_1_to_y_i={}
#y_iからy_i_plus_1の遷移の組み合わせを保存しておくリスト
y_i_to_y_i_plus_1={}
#y_iからx_iが生成される組み合わせを保存しておくリスト
y_i_to_x_i={}
#あり得るタグをすべて格納するリスト
tag_set=[]
#タグ番号0から21まで設定する
for tag_number in range(0, 21):tag_set.append(tag_number)

def preprocess_Y(tag_set, Y, input_file_lines):
    token_list=[]
    #token_listを作成しておく
    for line in input_file_lines:
        for token in line.strip('/n').split(): token_list.append(token)
    #多重ループになるけども，(y_i_-1,y_i),(y_i,y_i+1),(y_i,x_i)を作り出すためにこうする
    for y_i in tag_set:
        for y_i_minus_1 in tag_set:
            y_i_minus_1_to_y_i.setdefault(str(y_i_minus_1)+'_'+str(y_i), random.randint(0, 500))
        for y_i_plus_1 in tag_set:
            y_i_to_y_i_plus_1.setdefault(str(y_i)+'_'+str(y_i_plus_1), random.randint(0, 500))
        for x_i in token_list:
            y_i_to_x_i.setdefault(str(y_i)+'_'+x_i, random.randint(0, 500))
    Y.setdefault('y_i_minus_1_to_y_i', y_i_minus_1_to_y_i)
    Y.setdefault('y_i_to_x_i', y_i_to_x_i)
    Y.setdefault('y_i_to_y_i_plus_1', y_i_to_y_i_plus_1)
    return token_list, Y

def main():
    Y={}
    token_list, Y\
        =preprocess_Y(tag_set, Y, open('wiki-sample.word', 'r').readlines())
    for y_i in tag_set:
        sampletag.SampleTag(token_list, y_i, tag_set, Y)

if __name__=='__main__':
    main()
