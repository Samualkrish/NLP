# Decoding the data using Markov chain
from __future__ import division
import sys
import time
from math import log
import cPickle 

class DecodeModel:
    def __init__(self):
        self.transition = {}
        self.emission = {}
        self.tag = {}
        self.sentences =[]


    def read_learned_model(self, file):
        with open(file, "rb") as f:
            model = cPickle.loads(f.read())
            self.transition = model['transition']
            self.emission   = model['emission']
            self.tag        = model['tag']

    def read_from_raw_file(self, file):
        with open(file, "r") as f:
            self.sentences = f.read().splitlines()

    def decode(self):
        with open("hmmoutput.txt","w") as f:
            for sentence in self.sentences:
                pos = self.viterbi_decode(sentence)
                f.write(pos + "\n")

    def viterbi_decode(self, sentence):
        delta = [{},{}]
        backpointer = []
        words = "*S* " + sentence + " *T*"
        word_list = words.split(' ')
        
        # Initializing the word list
        delta[0] = {'ss':0}
        backpointer.append({'ss':'ss'})
        # Recursive algorithm
        i = 1
        length = len(word_list)
        while i < length:
            backpointer.append({})
            try:
                emi = self.emission[word_list[i]]
            except KeyError:
                if word_list[i] == "*T*":
                    emi = ["tt"]
                else:
                    emi = self.tag 
            for t in emi:
                li = {}
                for j in delta[0]:
                    tr = self.transition[j][t]
                    de = delta[0][j]
                    try:
                        em = self.emission[word_list[i-1]][j]
                        max_delta = log(tr,10) + log(em, 10) + de 
                    except KeyError:
                        max_delta = log(tr,10) + de 
                    li[max_delta] = j
                max_value = max(li.keys())
                delta[1][t] = max_value
                backpointer[i][t] =  li[max_value]
            delta[0] = dict(delta[1])
            delta[1] = dict()
            i = i + 1
        i = i - 1
        tag = 'tt'
        tagged_word = []
        while i > 1:
            try:
                pos = backpointer[i][tag]
                word = word_list[i-1] + "/" + pos
                tagged_word.append(word)
                tag = pos
                i = i - 1
            except KeyError:
                break

        tagged_word.reverse()
        return ' '.join(tagged_word)

if __name__ == '__main__':
    start_time = time.time()
    decoding = DecodeModel()
    decoding.read_learned_model("hmmmodel.txt")
    decoding.read_from_raw_file(sys.argv[1])
    decoding.decode()
    print("--- Execution time is %s seconds ---" %(time.time() - start_time))