#-*- coding:utf-8 -*-

import sys, random
import sampletag

#イテレーション数は適当に
N=10
#y_iのタグを保存しておくリスト
tag_of_y_i=[]
#y_i自身の頻度を保存しておく
frequency_y_i={}
#y_i_-1からy_iの遷移の組み合わせを保存しておく
frequency_y_i_minus_1_to_y_i={}
#y_iからy_i_plus_1の遷移の組み合わせを保存しておく
frequency_y_i_to_y_i_plus_1={}
#y_iからx_iが生成される組み合わせを保存しておく
frequency_y_i_to_x_i={}
#あり得るタグをすべて格納するリスト
tag_set=[]
#タグ番号0から21まで設定する
for tag_number in range(0, 22):tag_set.append(tag_number)

def preprocess_Y(tag_set, Y, input_file_lines):
    token_list=[]
    #token_listを作成しておく
    for line in input_file_lines:
        for token in line.strip('/n').split(): token_list.append(token)
    token_number=len(token_list)
    #y_0からy_maxまで適当にタグを割り当てる．タグは0~21だから乱数で与える
    for y_i in range(0, token_number): tag_of_y_i.append(random.randint(0, 21))
    #あり得るtagのbigramをすべて辞書として定義しておく．
    #多重ループになるけども，(y_i_-1,y_i),(y_i,y_i+1),(y_i,x_i)を作り出すためにこうする
    for y_i in tag_set:
        frequency_y_i.setdefault(str(y_i), 0)
        for y_i_minus_1 in tag_set:
            frequency_y_i_minus_1_to_y_i.setdefault(str(y_i_minus_1)+'_'+str(y_i), 0)
        for y_i_plus_1 in tag_set:
            frequency_y_i_to_y_i_plus_1.setdefault(str(y_i)+'_'+str(y_i_plus_1), 0)
        for x_i in token_list:
            frequency_y_i_to_x_i.setdefault(str(y_i)+'_'+x_i, 0)
    #unigram, bigramのカウントを取る
    for y_i, tag in enumerate(tag_of_y_i):
        frequency_y_i[str(tag)]+=1
        forward_bigram_key=str(tag_of_y_i[(y_i)-1])+'_'+str(tag)
        frequency_y_i_minus_1_to_y_i[forward_bigram_key]+=1
        generate_key=str(tag)+'_'+token_list[y_i]
        frequency_y_i_to_x_i[generate_key]+=1
        if y_i < len(tag_of_y_i)-1:
            backward_bigram_key=str(tag)+'_'+str(tag_of_y_i[(y_i)+1])
            frequency_y_i_to_y_i_plus_1[backward_bigram_key]+=1
        else:
            frequency_y_i_to_y_i_plus_1.setdefault(y_i, 1)
    #全部，Yの下に格納
    Y.setdefault('sequence_y_i', tag_of_y_i)
    Y.setdefault('frequency_y_i', frequency_y_i)
    Y.setdefault('frequency_y_i_minus_1_to_y_i', frequency_y_i_minus_1_to_y_i)
    Y.setdefault('frequency_y_i_to_x_i', frequency_y_i_to_x_i)
    Y.setdefault('frequency_y_i_to_y_i_plus_1', frequency_y_i_to_y_i_plus_1)
    return token_list, Y

def main():
    Y={}
    token_list, Y\
        =preprocess_Y(tag_set, Y, open('wiki-sample.word', 'r').readlines())
    for y_i, tag_of_y_i in enumerate(Y['sequence_y_i']):
        sampletag.SampleTag(token_list, y_i, Y, tag_set)

if __name__=='__main__':
    main()
