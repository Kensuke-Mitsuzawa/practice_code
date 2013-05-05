#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys

def call_mecab():
    import sys
    reload(sys)
    
    sys.setdefaultencoding('utf-8')

    import MeCab
    mecab = MeCab.Tagger('-Ochasen')

    i_file = 'mayu.txt'
    data = open( i_file ).read()

    node = mecab.parseToNode( data )
    phrases = node.next
    words = {}
    num = 0;
    #print "node is:",node

    while phrases:
        try:
            #print node.surface
            k = node.surface
            k = k.strip().rstrip()
            #print "k is:",k
            if k in words:
                """
                if words(dic) has k already
                """
                pass
            else:
                """
                if words(dic) does not have k, start by count 0
                """
                words[k] = num;
                num = num + 1
            
            node = node.next
            #print "now node is:",node
            
        except AttributeError:
            break

    #print "Finally,dictionary words:",words
    
    check_yabya(words)

def check_yabya(words):
    """

    input: words ; dictionary type
   
    """
    # if 0 no 「やびゃあ」, if 1 「やびゃあ」
    yaba = {0:"",1:""}
    
    count = 0
    tmp_condition = 0
    for i in yaba.keys():
        count = 0
        if i == 0:
            while tmp_condition == 0:
                try:
                    each_input = "./each_art/mayu" + "_" + str(count)
                    input_f = open(each_input,'r').readlines()
                    attr = make_attr_dic(input_f,words)
            
                    #print each_input,"file fin"
                    feat_num_list = []
                    for key_attr in sorted(attr.keys()):
                        feat_num =  str(key_attr)+":"+str(attr[key_attr])
                        feat_num_list.append(feat_num)
                    print i," ".join(feat_num_list)
                    count = count + 1
                except IOError:
                    break
                    

        if i ==  1:
            while tmp_condition == 0:
                try:
                    yaba_input = "./each_art/mayu" + "_" + "ya" + str(count)
                    input_f = open(yaba_input,'r').readlines()
                    make_attr_dic(input_f,words)

                    feat_num_list = []
                    for key_attr in sorted(attr.keys()):
                        feat_num =  str(key_attr)+":"+str(attr[key_attr])
                        feat_num_list.append(feat_num)
                    print i," ".join(feat_num_list)

                    count = count + 1
                except IOError:
                    break
    
def make_attr_dic(input_f,words):
    import MeCab
    mecab = MeCab.Tagger('-Ochasen')
    
    for line in input_f:
        """
        #set same condition in key of yaba(dic)
        """
        line = line.strip().rstrip()
        n = mecab.parseToNode( line )
        p = n.next
            
        # id dictionary for generation feather number
        attr = {}
            
        while p:
            try:
                k = n.surface
                if k not in words:
                    break
                id = words[k]
                if id in attr:
                    """
                    #if feather number dictionary already has id, +1 and regist in attr
                    """
                    attr[id] = attr[id] + 1
                else:
                    attr[id] = 1
                        
                n = n.next

            except AttributeError:
                break

    return attr


if __name__ == '__main__':
    call_mecab()
