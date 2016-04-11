# Decoding the data using Markov chain
from __future__ import division
import sys
import time
import json
from math import log
import cPickle 
from multiprocessing import Process

class Viterbi:
    def __init__(self):
        self.emission   = {}
        self.transition = {}

    def decode(self):
        f = open("file1.txt","w+")
        g = open("file2.txt","w+")
        delta = {}
        backpointer = {}
        words = "*S* " + words
        word_list = words.split()
        length = len(word_list)
        # Initializing the word list
        delta[0] = {'s':1}
        # Recursive algorithm
        for i, word in enumerate(word_list, start = 1):
            delta[i] = {}
            backpointer[i] = {}
            for t in self.tag:
                li = {}
                for j in delta[i-1]:
                    max_delta = log(self.transition[j][t],10) + log(self.emission[j][word],10) + delta[i-1][j]
                    li[j] = max_delta
                max_value = max(li.values())
                delta[i][t] = max_value
                for k in li:
                    if li[k] == max_value:
                        backpointer[i][t] =  k
                        break
        f.write(delta)
        g.write(backpointer)
        f.close()
        g.close()

class DecodeModel:
    def __init__(self):
        self.transition = {}
        self.emission = {}
        self.tag = {}
        self.word = {}
        self.sentences =[]


    def read_learned_model(self, file):
        with open(file, "rb") as f:
            model = cPickle.loads(f.read())
            self.transition = model['transition']
            self.emission   = model['emission']
            self.tag        = model['tag']
            self.word       = model['word']

    def read_from_raw_file(self, file):
        with open(file, "r") as f:
            self.sentences = f.read().splitlines()
            for s in self.sentences:
                words = s.split()
                for w in words:
                    if w not in self.word:
                        self.word[w] = 0

    def smooth_model(self):
        for t in self.emission:
            for w in self.word:
                if w in self.emission[t]:
                    self.emission[t][w] += 1
                else:
                    self.emission[t][w] = 1
                self.tag[t] += self.emission[t][w]
            for w in self.word:
                self.emission[t][w] = self.emission[t][w]/self.tag[t]
        self.emission['s'] = {'*S*':1}

    def get_semantic(self, sentence):
        semantic = {}
        sen = sentence.split()
        for s in sen:
            semantic[s] = {}
            for t in self.tag:
                semantic[s][t] = 0
        return semantic

    def viterbi_algo(self):
        self.tag.pop("s",None)
        t_value = self.tag['t']
        self.tag.pop("t",None)
        f = open("hmmoutput.txt","w+")
        start_time = time.time()
        for line, words in enumerate(self.sentences):
            delta = []
            backpointer = []
            words = "*S* " + words
            word_list = words.split()
            length = len(word_list)
            # Initializing the word list
            # delta[0] = {'s':1}
            delta.append({'s':1})
            backpointer.append({'s':'s'})
            # Recursive algorithm
            for i, word in enumerate(word_list, start = 1):
                delta.append({})
                backpointer.append({})
                # if i == length -1 :
                #     self.tag["t"] = t_value
                for t in self.tag:
                    li = {}
                    for j in delta[i-1]:
                        max_delta = log(self.transition[j][t],10) + log(self.emission[j][word],10) + delta[i-1][j]
                        li[max_delta] = j
                    max_value = max(li.keys())
                    delta[i][t] = max_value
                    # for k in li:
                    #     if li[k] == max_value:
                    backpointer[i][t] =  li[max_value]
                            # break
            delta.append({})
            backpointer.append({})
            li = {}
            for j in delta[length-1]:
                max_delta = log(self.transition[j]['t'],10) + log(self.emission[j][word],10) + delta[i-1][j]
                li[max_delta] = j
            max_value = max(li.keys())
            delta[i+1]['t'] = max_value
            # for k in li:
            #     if li[k] == max_value:
            backpointer[i+1]['t'] =  li[max_value]
                    # break
            print("Execution Time for a sentence is %s seconds" %(time.time() - start_time))
            start_time = time.time()

            pos = backpointer[i+1]['t']
            pos_sentence = []
            for i in range(len(word_list)-1, 0, -1):
                pos_sentence.append(word_list[i] + "/" +  pos)
                pos = backpointer[i][pos]

            pos_sentence.reverse()
            f.write(' '.join(pos_sentence) + "\n")
        f.close()
            


if __name__ == '__main__':
    start_time = time.time()
    decoding = DecodeModel()
    decoding.read_learned_model("hmmmodel.txt")
    decoding.read_from_raw_file(sys.argv[1])
    decoding.smooth_model()
    decoding.viterbi_algo()
    print("--- Execution time is %s seconds ---" %(time.time() - start_time))
