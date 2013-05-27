#! /usr/bin/python
# -*- coding:utf-8 -*-
__version__='2013/5/25'

alpha=0.1

def dirichlet_process(tag, y_i, token_list, Y):
   frequency_of_y_i_minus_1=Y['frequency_y_i'][str(Y['sequence_y_i'][(y_i)-1])]
   frequency_of_y_i=Y['frequency_y_i'][str(Y['sequence_y_i'][y_i])]
   """
   #TODO:残りのパラメータも準備してdiriclet processの式の完成
   #基底確率について：P_base,Tは一様分布に．P_base_Eは単語のユニグラム確率にする
   本当は，y_(i-1)が名詞のとき，y_iの品詞が〜にである確率．\
       という風に基底測度を分けた方がよいのかもしれないが...\
       ここでは面倒なので，すべてのタグが完全に一様分布とする\
       つまりどの品詞タグも1/21で出現
       """
   base_measure_T=1.0/21
   #要は基底測度
   base_measure_E=Y['unigram_prob'][token_list[y_i]]
   
   print base_measure_T, base_measure_E

def SampleTag(token_list, y_i, Y, tag_set):
   """
   y_iはY['sequence_y_i']のリストのインデックス番号
   token_listはcorpusのtoken区切りのリスト
   tag_setはタグの集合
   """
   #確率を格納するリスト
   p=[]
   #--------------------------------------------------------------------------------------------------------
   #いまのタグのカウントを−１する（グラム先生のスライドには削除って書いてあるけど，たぶん間違いだと思うんだ）
   forward_bigram_key=str(Y['sequence_y_i'][y_i-1])+'_'+str(Y['sequence_y_i'][y_i])
   Y['frequency_y_i_minus_1_to_y_i'][forward_bigram_key]-=1
   generate_key=str(Y['sequence_y_i'][y_i])+'_'+str(token_list[y_i])
   Y['frequency_y_i_to_x_i'][generate_key]-=1
   if y_i < len(Y['sequence_y_i'])-1:
      backward_bigram_key=str(Y['sequence_y_i'][y_i])+'_'+str(Y['sequence_y_i'][(y_i)+1])
      Y['frequency_y_i_to_y_i_plus_1'][backward_bigram_key]-=1
   else:
       Y['frequency_y_i_to_y_i_plus_1'].setdefault(y_i, 1)
    #--------------------------------------------------------------------------------------------------------

   for tag in tag_set:
      p.append(dirichlet_process(tag, y_i, token_list, Y))
   #y_i=SampleOne(p)

