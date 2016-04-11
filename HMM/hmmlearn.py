from __future__ import division
import sys
import cPickle
import time
import json

class Model:
    def __init__(self):
        self.model = []
        self.emission = {}
        self.transition = {}
        self.tag = {}
        self.word = {}
        self.output = {}
        self.sentences = []

    def read_from_file(self, file):
        with open(file, "r") as f:
            self.sentences = f.read().splitlines()

    def add_to_emission(self, tag, word):
        if tag in self.emission:
            if word in self.emission[tag]:
                self.emission[tag][word] += 1
            else:
                self.emission[tag][word] = 1
        else:
            self.emission[tag] = {word:1}

    def add_to_transition(self, current_tag, next_tag):
        if current_tag in self.transition:
            if next_tag in self.transition[current_tag]:
                self.transition[current_tag][next_tag] += 1
            else:
                self.transition[current_tag][next_tag] = 1
        else:
            self.transition[current_tag] = {next_tag:1}

    def build_semantics(self):
        self.tag['s'] = 0
        self.tag['t'] = 0
        for line in self.sentences:
            current_pos = 's'
            word_pos = line.split()
            for word in word_pos:
                w = word[0:-3]
                t = word[-2:]
                if t not in self.tag:
                    self.tag[t] = 0
                if w not in self.word:    
                    self.word[w] = 0

                # Add to the emission matrix
                self.add_to_emission(t,w)

                # Add to the transition matrix
                next_pos = t
                self.add_to_transition(current_pos,next_pos)
                current_pos = next_pos
            #Add the transition matrix for terminal state
            next_pos = 't'
            self.add_to_transition(current_pos,next_pos)

    def build_emission(self):
        for line in self.sentences:
            word_pos = line.split()
            for word in word_pos:
                w = word[0:-3]
                t = word[-2:]
                if w in self.emission[t]:
                    self.emission[t][w] += 1
                else:
                    self.emission[t][w] = 1
        
    def build_transition(self):
        '''Builds the transition probability matrix.'''

        for line in self.sentences:
            word_pos = line.split()
            current_pos = 's'
            for word in word_pos:
                next_pos = word[-2:]
                self.transition[current_pos][next_pos] += 1 
                current_pos = next_pos
            next_pos = 't'
            self.transition[current_pos][next_pos] += 1 

    def smooth_transition(self):
        for i in self.transition:
            self.transition[i]['total'] = 0
            for j in self.tag:
                if j == 's':
                    self.transition[i][j] = 0
                elif j not in self.transition[i]:
                    self.transition[i][j] = 1
                else:
                    self.transition[i][j] += 1
                self.transition[i]['total'] += self.transition[i][j]
            for j in self.tag:
                self.transition[i][j] = self.transition[i][j] / self.transition[i]['total']


    def build_output(self):
        self.output['emission'] = self.emission
        self.output['transition'] = self.transition
        self.output['tag'] = self.tag
        self.output['word'] = self.word

    def create_hmm(self):
        self.build_semantics()
        self.smooth_transition()
        self.build_output()

    def write_to_output(self, file):
        with open(file, "wb") as f:
            cPickle.dump(self.output, f, protocol=cPickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    start_time = time.time()
    model = Model()
    model.read_from_file(sys.argv[1])
    model.create_hmm()
    model.write_to_output("hmmmodel.txt")
    print("Total Execution Time is %s " % (time.time() - start_time))