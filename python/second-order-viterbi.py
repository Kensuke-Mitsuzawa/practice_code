#/usr/bin/python
# -*- coding:utf-8 -*-
# code was in http://prashanth-kamle.blogspot.jp/2009/03/viterbi-algorithm-for-second-order.html?m=1

states = ('Rainy','Sunny')

observations = ('walk','shop','clean')

start_probability = {
    'Rainy|Rainy':0.7,
    'Rainy|Sunny':0.3,
    'Sunny|Rainy':0.4,
    'Sunny|Sunny':0.6
    }

transition_probability = {
    'Rainy|Rainy' : {'Rainy':0.8,'Sunny':0.2},
    'Rainy|Sunny' : {'Rainy':0.5,'Sunny':0.5},
    'Sunny|Rainy' : {'Rainy':0.6,'Sunny':0.4},
    'Sunny|Sunny' : {'Rainy':0.3,'Sunny':0.7},
}

emission_probability = {
    'Rainy' : {'walk':0.1,'shop':0.4,'clean':0.5},
    'Sunny' : {'walk':0.6,'shop':0.3,'clean':0.1},
    }

def forward_viterbi(obs,states,start_p,trans_p,emit_p):
    #---------------------------------------------------------------------------
    # Tには考えられる遷移確率の組と生成確率の組を記録する
    T = {}
    #記録を行うのはこの下の２つのfor文とその下の代入式。Tは辞書型でキーに遷移先｜遷移前、値に（開始確率、遷移前状態名、開始確率の三つ組み）
    for state1 in states:
        for state2 in states:
            T[state1+"|"+state2] = (start_p[state1+"|"+state2],[state2],start_p[state1+"|"+state2])
            print T
     #---------------------------------------------------------------------------

        
    
    for output in obs:
        U = {}
        print "---------------------------------\nObservation:",output
        for next_state in states:
            total = 0
            argmax = None
            valmax = 0
            print "Next state:" + next_state
            for curr_state in states:
                for prv_state in states:
                    print '\t#--------------------------------------------'
                    print "\tNow curr state is:",curr_state
                    print "\tNow prv state is:",prv_state
                    print "\tprv_state|curr_state:",prv_state+"|"+curr_state
                    
                    try:
                        (prob,v_path,v_prob) = T[prv_state+"|"+curr_state]
                    except KeyError:
                        (prob,v_path,v_prob) = T[prv_state+"|"+curr_state]=(0,None,0)

                    print '\temit is---',emit_p
                    print '\ttrans is---',trans_p
                    
                    #s_t-1からs_tへの遷移をする時に、~の確率*s_tからo_tが生成される確率。という計算を下の式で行う。
                    #v_probで一個前のイテレーションで記録されていた確率に掛け合わせる。
                    #もし、現時点で最高数値(valmaxに記録)の確率よりもv_probが高い確率になれば、その時はその数字を最高とするパスを取る。
                    p = emit_p[curr_state][output]*trans_p[prv_state+"|"+curr_state][next_state]
                    print "\tnow emission prob.---",emit_p[curr_state][output]
                    print "\tnow transition prob.---",trans_p[prv_state+"|"+curr_state][next_state]
                    
                    
                    prob *= p
                    print "\tnow total prob. is",prob
                    v_prob *= p
                    total += prob
                    print "\tnow summation of prob. is",total

                    #もし、現時点で最高数値(valmaxに記録)の確率よりもv_probが高い確率になれば、その時はその数字を最高とするパスを取る。
                    #そして現時点で最高の数字でたどって来た経路（最尤経路）での合計確率値をargmaxに記録しておく
                    if v_prob > valmax:
                        argmax = v_path+[next_state]
                        valmax = v_prob
                    
                    print "\t\t",v_path,v_prob

                U[curr_state+"|"+next_state] = (total,argmax,valmax)
                print "\targmax:",argmax,"valmax:",valmax

            T=U
##apply sum/max to the final states:
    total = 0
    atgmax = None
    valmax = 0
    for state1 in states:
        for state2 in states:
            try:
                (prob,v_path,v_prob) = T[state1+"|"+state2]
            except KeyError:
                (prob,v_path,v_prob) = T[state1+"|"+state2]=(0,None,0)
            total += prob
        
            if v_prob > valmax:
                argmax = v_path
                valmax = v_prob
            
    return (total,argmax,valmax)

def example():
    return forward_viterbi(observations,states,start_probability,transition_probability,emission_probability)

res = example()
print '\nResult:',res
