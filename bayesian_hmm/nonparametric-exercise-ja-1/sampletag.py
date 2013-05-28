#! /usr/bin/python
# -*- coding:utf-8 -*-
__version__='2013/5/27'

import sampleone

alpha=0.01

def dirichlet_process(tag, y_i, token_list, Y):
   frequency_of_y_i_minus_1=Y['frequency_y_i'][str(Y['sequence_y_i'][(y_i)-1])]
   frequency_of_y_i=Y['frequency_y_i'][str(Y['sequence_y_i'][y_i])]
   #y_(i-1)がそのままだとインデックスの最後を参照してしまうので以下の処理
   if y_i>0:
      frequency_y_i_minus_1_to_y_i=\
          Y['frequency_y_i_minus_1_to_y_i'][str(Y['sequence_y_i'][(y_i)-1])+'_'+str(tag)]
   else:frequency_y_i_minus_1_to_y_i=Y['frequency_y_i_minus_1_to_y_i'][str(tag)]
   if y_i < len(Y['sequence_y_i'])-1:
      frequency_y_i_to_y_i_plus_1=\
          Y['frequency_y_i_to_y_i_plus_1'][str(tag)+'_'+str(Y['sequence_y_i'][(y_i)+1])]
   else:frequency_y_i_to_y_i_plus_1=Y['frequency_y_i_to_y_i_plus_1'][str(tag)]
   frequency_y_i_to_x_i=Y['frequency_y_i_to_x_i'][str(tag)+'_'+str(token_list[y_i])]
   """
   #基底確率について：P_base,Tは一様分布に．P_base_Eは単語のユニグラム確率にする
   本当は，y_(i-1)が名詞のとき，y_iの品詞が〜にである確率．\
       という風に基底測度を分けた方がよいのかもしれないが...\
       ここでは面倒なので，すべてのタグが完全に一様分布とする\
       つまりどの品詞タグも1/21で出現
       """
   base_measure_T=1.0/21
   #要はunigram確率
   base_measure_E=Y['unigram_prob'][token_list[y_i]]
   #dirichlet_process equations below
   p_tag_given_y_i_minus_1=(frequency_y_i_minus_1_to_y_i+alpha*base_measure_T)/(frequency_of_y_i_minus_1+alpha)
   p_y_i_plus_1_given_tag=(frequency_y_i_to_y_i_plus_1+alpha*base_measure_T)/(frequency_of_y_i+alpha)
   p_x_i_given_tag=(frequency_y_i_to_x_i+alpha*base_measure_E)/(frequency_of_y_i+alpha)
   p_multiplicated=(p_tag_given_y_i_minus_1)*(p_y_i_plus_1_given_tag)*(p_x_i_given_tag)
   return p_multiplicated
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
   generate_key=str(Y['sequence_y_i'][y_i])+'_'+str(token_list[y_i])
   Y['frequency_y_i_to_x_i'][generate_key]-=1
   #y_(i-1)がそのままだとインデックスの最後を参照してしまうので以下の処理
   if y_i>0:
      forward_bigram_key=str(Y['sequence_y_i'][y_i-1])+'_'+str(Y['sequence_y_i'][y_i])
      Y['frequency_y_i_minus_1_to_y_i'][forward_bigram_key]-=1
   else:Y['frequency_y_i_minus_1_to_y_i'][str(Y['sequence_y_i'][y_i])]-=1
   if y_i < len(Y['sequence_y_i'])-1:
      backward_bigram_key=str(Y['sequence_y_i'][y_i])+'_'+str(Y['sequence_y_i'][(y_i)+1])
      Y['frequency_y_i_to_y_i_plus_1'][backward_bigram_key]-=1
   else:Y['frequency_y_i_to_y_i_plus_1'][str(Y['sequence_y_i'][y_i])]-=1
    #--------------------------------------------------------------------------------------------------------

   for tag in tag_set:
      p.append(dirichlet_process(tag, y_i, token_list, Y))
   y_i=sampleone.SampleOne(p)

   if isinstance(y_i, int)==True:  
      Y['frequency_y_i'][str(y_i)]+=1
      #y_(i-1)がそのままだとインデックスの最後を参照してしまうので以下の処理
      if y_i>0:
         forward_bigram_key=str(Y['sequence_y_i'][y_i-1])+'_'+str(Y['sequence_y_i'][y_i])
         Y['frequency_y_i_minus_1_to_y_i'][forward_bigram_key]+=1
      else:Y['frequency_y_i_minus_1_to_y_i'][str(tag)]+=1
      if y_i < len(Y['sequence_y_i'])-1:
         backward_bigram_key=str(Y['sequence_y_i'][y_i])+'_'+str(Y['sequence_y_i'][(y_i)+1])
         Y['frequency_y_i_to_y_i_plus_1'][backward_bigram_key]+=1
      else:Y['frequency_y_i_to_y_i_plus_1'][str(Y['sequence_y_i'][y_i])]+=1
      Y['frequency_y_i_to_x_i'][str(Y['sequence_y_i'][y_i])+'_'+token_list[y_i]]+=1
   elif y_i==True:
      pass
   return Y
