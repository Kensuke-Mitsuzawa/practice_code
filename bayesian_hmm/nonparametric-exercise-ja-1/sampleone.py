#-*- coding:utf-8 -*-

def sampleone(probs):
    z=sum(probs)
    remaining=rand(z)
    for i in range(1, len(probs)):
        remaining-=probs[i]
        if remaining<=0:
            return i
