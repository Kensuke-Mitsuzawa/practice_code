#-*- coding:utf-8 -*-
import random

def SampleOne(probs):
    z=sum(probs)
    remaining=random.uniform(0, z)
    for i in range(1, len(probs)):
        remaining-=probs[i]
        if remaining<=0:
            #これって，もしremainingの方が最後まで大きかったらどうするんだろう？サンプリング失敗ってことでpassする？
            return i
