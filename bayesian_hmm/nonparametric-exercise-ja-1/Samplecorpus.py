#-*- coding:utf-8 -*-

import sys, random

#イテレーション数は適当に
N=10
#タグ:確率を格納する辞書Yの定義とランダム値での初期化
Y={}
for i in range(0, 21):
    random_value=random.random()
    Y.setdefault('y_'+str(i), random_value)

for i in range(0, N):
    print i
