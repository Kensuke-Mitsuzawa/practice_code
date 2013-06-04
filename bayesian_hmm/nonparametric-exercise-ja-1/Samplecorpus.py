#-*- coding:utf-8 -*-

import sys, random
import sampletag

#イテレーション数は適当に
N=1
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
#x_iのunigram確率を保存しておく
unigram_prob={}
#theta_parameter dictionary
theta_parameter={}
#タグ番号0から21まで設定する
for tag_number in range(0, 22):tag_set.append(tag_number)

def count_x_i(word, token_list):
   count=0
   for x_i in token_list:
      if x_i == word: count+=1
      else: pass 
   unigram_prob=float(count)/len(token_list)
   return 

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
          frequency_y_i_minus_1_to_y_i.setdefault(str(y_i_minus_1), 0)
       for y_i_plus_1 in tag_set:
          frequency_y_i_to_y_i_plus_1.setdefault(str(y_i)+'_'+str(y_i_plus_1), 0)
          frequency_y_i_to_y_i_plus_1.setdefault(str(y_i_plus_1), 0)
       for x_i in token_list:
          frequency_y_i_to_x_i.setdefault(str(y_i)+'_'+x_i, 0)
    #unigram, bigramのカウントを取る
    for y_i, tag in enumerate(tag_of_y_i):
       frequency_y_i[str(tag)]+=1
       generate_key=str(tag)+'_'+token_list[y_i]
       frequency_y_i_to_x_i[generate_key]+=1
       #y_(i-1)がそのままだとインデックスの最後を参照してしまうので以下の処理
       if y_i>0:
          forward_bigram_key=str(tag_of_y_i[(y_i)-1])+'_'+str(tag)
          frequency_y_i_minus_1_to_y_i[forward_bigram_key]+=1
       else:
          frequency_y_i_minus_1_to_y_i[str(tag)]+=1
       #y_(i+1)が存在するtoken数より大きくなることがあるので，以下の処理
       if y_i < len(tag_of_y_i)-1:
          backward_bigram_key=str(tag)+'_'+str(tag_of_y_i[(y_i)+1])
          frequency_y_i_to_y_i_plus_1[backward_bigram_key]+=1
       else:
          frequency_y_i_to_y_i_plus_1[str(tag)]+=1
    #unigramを確率を計算しておく        
    for x_i in token_list:
       if not x_i in unigram_prob: unigram_prob.setdefault(x_i, 1)
       else: unigram_prob[x_i]+=1
    for x_i in unigram_prob: unigram_prob[x_i]=float(unigram_prob[x_i])/len(token_list)        
    #全部，Yの下に格納
    Y.setdefault('sequence_y_i', tag_of_y_i)
    Y.setdefault('frequency_y_i', frequency_y_i)
    Y.setdefault('frequency_y_i_minus_1_to_y_i', frequency_y_i_minus_1_to_y_i)
    Y.setdefault('frequency_y_i_to_x_i', frequency_y_i_to_x_i)
    Y.setdefault('frequency_y_i_to_y_i_plus_1', frequency_y_i_to_y_i_plus_1)
    Y.setdefault('unigram_prob', unigram_prob)
    return token_list, Y
def calculate_theta_parameter(Y, summation_dict, token_list):
   """
   theta parameterつまり遷移確率と生成確率を計上する
   """
   transition_prob_y_i_minus_1_to_y_i={}
   transition_prob_y_i_to_y_i_plus_1={}
   emission_prob_y_i_to_x_i={}
   for y_i_minus_1 in range(0, 21):
      for y_i in range(0, 21):
         transition_prob_y_i_minus_1_to_y_i.setdefault('{0}_{1}'.format(y_i_minus_1, y_i),\
                                                          Y['frequency_y_i_minus_1_to_y_i']['{0}_{1}'.format(y_i_minus_1, y_i)]/float(summation_dict['sum_y_i_minus_1_to_y_i_set']['frequency_{0}_to_any'.format(y_i_minus_1)]) )
   for y_i in range(0, 21):
      for y_i_plus_1 in range(0, 21):
         transition_prob_y_i_to_y_i_plus_1.setdefault('{0}_{1}'.format(y_i, y_i_plus_1),\
                                                         Y['frequency_y_i_to_y_i_plus_1']['{0}_{1}'.format(y_i, y_i_plus_1)]/float(summation_dict['sum_y_i_to_y_i_plus_1_set']['frequency_{0}_to_any'.format(y_i)]) )
   
   for y_i_minus_1 in range(0, 21):
      for x_token in token_list:
         emission_prob_y_i_to_x_i.setdefault('{0}_{1}'.format(y_i, x_token),\
                                                Y['frequency_y_i_to_x_i']['{0}_{1}'.format(y_i, x_token)]/float(summation_dict['sum_y_i_minus_1_to_y_i_set']['frequency_{0}_to_any'.format(y_i)]) )
   print emission_prob_y_i_to_x_i
def summation_transition_and_emission_frequency(Y, token_list):
   """
   theta parameterを求めるときの分母に使う数を計上する
   """
   summation_dict={}
   transition_freq_y_i_minus_1_to_any_set={}
   transition_freq_y_i_to_any_set={}
   emission_freq_y_i_to_any_set={}
   for y_i_minus_1 in range(0, 21):
      key_of_freq_y_i_minus_1_to_any='frequency_{0}_to_any'.format(y_i_minus_1)
      transition_freq_y_i_minus_1_to_any_set.setdefault(key_of_freq_y_i_minus_1_to_any, 0)
      for y_i in range(0, 21):
         transition_freq_y_i_minus_1_to_any_set[key_of_freq_y_i_minus_1_to_any]+=\
             Y['frequency_y_i_minus_1_to_y_i']['{0}_{1}'.format(y_i_minus_1, y_i)]
   for y_i in range(0, 21):
      key_of_freq_y_i_to_any='frequency_{0}_to_any'.format(y_i)
      transition_freq_y_i_to_any_set.setdefault(key_of_freq_y_i_to_any, 0)
      for y_i_plus_1 in range(0, 21):
         transition_freq_y_i_to_any_set[key_of_freq_y_i_to_any]+=\
             Y['frequency_y_i_minus_1_to_y_i']['{0}_{1}'.format(y_i, y_i_plus_1)]
   for y_i in range(0, 21):
      key_of_freq_y_i_to_any_x='frequency_{0}_to_any_x'.format(y_i)
      emission_freq_y_i_to_any_set.setdefault(key_of_freq_y_i_to_any_x, 0)
      for x_token in token_list:
         emission_freq_y_i_to_any_set[key_of_freq_y_i_to_any_x]+=\
             Y['frequency_y_i_to_x_i']['{0}_{1}'.format(y_i, x_token)]
   summation_dict.setdefault('sum_y_i_to_x_i_set', emission_freq_y_i_to_any_set)
   summation_dict.setdefault('sum_y_i_to_y_i_plus_1_set', transition_freq_y_i_to_any_set)
   summation_dict.setdefault('sum_y_i_minus_1_to_y_i_set', transition_freq_y_i_minus_1_to_any_set)
   return summation_dict

def debug(Y):
   all_frequency_y_i_minus_1_to_y_i=0
   all_frequency_y_i_to_y_i_plus_1=0
   all_frequency_y_i_to_x_i=0
   for y_i_minus_1_to_y_i in Y['frequency_y_i_minus_1_to_y_i']:\
          all_frequency_y_i_minus_1_to_y_i+=Y['frequency_y_i_minus_1_to_y_i'][y_i_minus_1_to_y_i]
   for y_i_to_y_i_plus_1 in Y['frequency_y_i_to_y_i_plus_1']:\
          all_frequency_y_i_to_y_i_plus_1+=Y['frequency_y_i_to_y_i_plus_1'][y_i_to_y_i_plus_1]
   for y_i_to_x_i in Y['frequency_y_i_to_x_i']:
      all_frequency_y_i_to_x_i+=Y['frequency_y_i_to_x_i'][y_i_to_x_i]
      if Y['frequency_y_i_to_x_i'][y_i_to_x_i]>1000: print y_i_to_x_i
   print "y_(i-1) to y_i", all_frequency_y_i_minus_1_to_y_i
   print "y_i to x_i", all_frequency_y_i_to_x_i
   print "y_i to y_(i+1)", all_frequency_y_i_to_y_i_plus_1


def main():
   Y={}
   theta_list=[]
   token_list, Y\
       =preprocess_Y(tag_set, Y, open('wiki-sample.word_edit', 'r').readlines())
   for iter_i in range(0, N):
      for y_i in (Y['sequence_y_i']):
         Y=sampletag.SampleTag(token_list, y_i, Y, tag_set)
      summation_dict=summation_transition_and_emission_frequency(Y, token_list)
      theta_parameter=calculate_theta_parameter(Y, summation_dict, token_list)
      """
      theta_list.append(theta_parameter)
      debug(Y)
      """


if __name__=='__main__':
   main()
