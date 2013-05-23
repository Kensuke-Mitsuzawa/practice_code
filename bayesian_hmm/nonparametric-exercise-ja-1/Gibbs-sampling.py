#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
Gibbs samplingの実装。「道具としてのベイズ統計」のパラメータをそのまま流用。
"""
import sys, math, random
import numpy as np
import pylab as pl
import scipy.stats as stats

number_of_data=30
Q=138.22
average=5.11

n_0=0.02
S_0=1.0
mu_0=5.0
m_0=0.25

mu_1=(number_of_data*average+(m_0*mu_0))/(m_0+number_of_data)
m_1=30.25
n_1=float(number_of_data)
n_1_times_S_1=138.24
    
def sample_mu_from_normal_distri_of_after(sigma):
    mu_in_mu_distribution_after=mu_1
    sigma_in_mu_distribution_after=(sigma)/m_1
    mu_now=stats.norm.rvs(mu_in_mu_distribution_after, sigma_in_mu_distribution_after)
    return mu_now
def sample_sigma_from_inverse_gamma_distri_of_after(mu_now):
    mu_in_sigma_distribution_after=(n_1+1.0)/2.0
    sigma_in_sigma_distribution_after=((n_1_times_S_1)+m_1*((mu_now-mu_1)**2))/2.0
    #ちょっとこの関数には妙な感じがするので、別の方法で
    #sigma_now=stats.invgamma.rvs(sigma_in_sigma_distribution_after, loc=mu_in_sigma_distribution_after)
    #sigma_now=math.sqrt(sigma_now)
    sigma_now=(1.0/random.gammavariate(mu_in_sigma_distribution_after, 1.0/sigma_in_sigma_distribution_after))
    return sigma_now
def main(ITER_NUM):
    sigma_now=4.0
    mu_list=[]
    sigma_list=[]
    for i in range(0, ITER_NUM):
        mu_now=sample_mu_from_normal_distri_of_after(sigma_now)
        sigma_now=sample_sigma_from_inverse_gamma_distri_of_after(mu_now)
        mu_list.append(mu_now)
        sigma_list.append(sigma_now)    
    #サンプリングしたうち、はじめの1000個は使ってはいけないデータらしいので、捨てる
    del mu_list[0:999]
    del sigma_list[0:999]
    mu_summation=0
    for x in mu_list:mu_summation+=x
    average_mu=float(mu_summation)/len(mu_list)
    sigma_summation=0
    for x in sigma_list:sigma_summation+=x
    average_sigma=sigma_summation/len(sigma_list)
    print average_mu, average_sigma
if __name__=='__main__':
    main(ITER_NUM=3000)
