#! /usr/bin/python
# -*- coding:utf-8 -*-
__author__='Kensuke Mitsuzawa'

import sys, math

def train(trainfile):
    emit={}
    transition={}
    context={}
    #文頭記号
    previous=u'<s>'
    context.setdefault(previous, 1)
    for line in trainfile.readlines():
        conv_to_uni=lambda x:x.decode('utf-8')
        line=conv_to_uni(line)
        wordtags=line.strip(u'\n').split(u' ')
        for wordtag in wordtags:
            word, tag=wordtag.split(u'_')
            if previous+u' '+tag in transition: transition[previous+u' '+tag]+=1
            else: transition.setdefault(previous+u' '+tag, 1)
            if tag in context: context[tag]+=1
            else: context.setdefault(tag, 1)
            if tag+u' '+word in emit: emit[tag+u' '+word]+=1
            else: emit.setdefault(tag+u' '+word, 1)
            previous=tag
        if previous+u' </s>' in transition: transition[previous+u' </s>']+=1
        else: transition.setdefault(previous+u' </s>', 1)
    #以下はモデルの保存にために使うこともあるらしい（を意図しているようだ
    for key in transition:
        previous, word=key.split(u' ')
        print 'T', key, float(transition[key])/context[previous]
        transition[key]=float(transition[key])/context[previous]
    for key in emit:
        tag, word=key.split(u' ')
        print 'E', key, float(emit[key])/context[tag]
        emit[key]=float(emit[key])/context[tag]

    return emit, transition, context

def forward(testfile, emit, transition, context):
    for line in testfile.readlines():
        conv_to_uni=lambda x:x.decode('utf-8')
        words=conv_to_uni(line).strip('\n').split(u' ')
        L=len(words)
        best_score={}
        best_edge={}
        #best_edgeは移動したパスを記録していく．
        best_score['0 <s>']=0
        best_edge['0 <s>']='NULL'
        for i in range(0, L):
            for prev_tag in context:
                for next_tag in context:
                    #スコアが最小になるパスを選んでいるのがここ以下のコード
                    if u'{0} {1}'.format(i, prev_tag) in best_score\
                            and u'{0} {1}'.format(prev_tag, next_tag) in transition\
                            and u'{0} {1}'.format(next_tag, words[i]) in emit:
                        #socreっていう変数は現ノードから次のノードへのパススコアを計算している
                        score=best_score['{0} {1}'.format(i, prev_tag)]+ -1*(math.log(transition['{0} {1}'.format(prev_tag, next_tag)])+ -1*(math.log(emit['{0} {1}'.format(next_tag, words[i])])))
                        try:
                            if best_score['{0} {1}'.format(i+1, next_tag)]>score:
                                best_score['{0} {1}'.format(i+1, next_tag)]=score
                                best_edge['{0} {1}'.format(i+1, next_tag)]='{0} {1}'.format(i, prev_tag)
                        except KeyError:
                            if not '{0} {1}'.format(i+1, next_tag) in best_score:
                                best_score.setdefault('{0} {1}'.format(i+1, next_tag), score)
                                best_edge.setdefault('{0} {1}'.format(i+1, next_tag), '{0} {1}'.format(i, prev_tag))

        #最後，</s>に対して，最小のスコアを持つエッジをえらぶ
        for prev_tag in context:
            #スコアが最小になるパスを選んでいるのがここ以下のコード
            if '{0} {1}'.format(L, prev_tag) in best_score:
                if '{} </s>'.format(prev_tag) in transition:
                    #socreっていう変数は現ノードでのスコアを計算している
                    score=best_score['{0} {1}'.format(L, prev_tag)]+ -1*(math.log(transition['{0} </s>'.format(prev_tag)]))
                    try:
                        if best_score['{0} </s>'.format(L+1)]>score:
                            best_score['{0} </s>'.format(L+1)]=score
                            best_edge['{0} </s>'.format(L+1)]='{0} {1}'.format(L, prev_tag)
                    except KeyError:
                        if not '{0} </s>'.format(i) in best_score:
                            best_score.setdefault('{0} </s>'.format(L+1), score)
                            best_edge.setdefault('{0} </s>'.format(L+1), '{0} {1}'.format(L, prev_tag))
        print best_edge
        print best_score
        backward(best_edge, best_score, L)
    return best_edge, best_score, L

def backward(best_edge, best_score, L):
    tags=[]
    next_edge=best_edge['{} </s>'.format(L+1)]
    while next_edge!='0 <s>':
        position, tag=next_edge.split(' ')
        tags.append(tag)
        next_edge=best_edge[next_edge]
    tags.reverse()
    print ' '.join(tags)

def main():
    trainfile=open(sys.argv[1])
    emit, transition, context=train(trainfile)
    testfile=open(sys.argv[2])
    best_edge, best_score, L=forward(testfile, emit, transition, context)


if __name__=='__main__':
    main()
