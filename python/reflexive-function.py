# /usr/bin/python
# -*- coding:utf-8 -*-

#階乗の再帰関数
def fact(n):
    if n == 0: return 1
    return n * fact(n-1)

#最大公約数の再帰関数
def gcd(a,b):
    if b == 0 return a
    return gcd(b, a%b)

#最大公倍数の再帰関数
def lcm(a,b):
    return a * b/ gcd(a,b)

print fact(5)
