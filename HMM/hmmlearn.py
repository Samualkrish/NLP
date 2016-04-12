from __future__ import division
import sys
import cPickle
import time

class Model:
    def __init__(self):
        self.model = []
        self.emission = {}
        self.transition = {}
        self.tag = {}
        self.word = {}
        self.word_tag = {}
        self.output = {}
        self.sentences = []

    def read_from_file(self, file):
        with open(file, "r") as f:
            self.sentences = f.read().splitlines()

    def add_to_emission(self, tag, word):
        try:
            try:
                self.emission[word][tag] = self.emission[word][tag] + 1
            except KeyError:
                self.emission[word][tag] = 1
        except KeyError:
            self.emission[word] = {tag:1}

    def add_to_tag(self,tag):
        try:
            self.tag[tag] = self.tag[tag] + 1
        except KeyError:
            self.tag[tag] = 1

    def add_to_word_tag(self, word, tag):
        try:
            self.word_tag[word][tag] = 0
        except KeyError:
            self.word_tag[word] = {tag:0}

    def add_to_transition(self, current_tag, next_tag):
        try:
            try:
                self.transition[current_tag][next_tag] = self.transition[current_tag][next_tag] + 1
            except KeyError:
                self.transition[current_tag][next_tag] = 1
        except KeyError:
            self.transition[current_tag] = {next_tag:1}

    def add_unknown(self):
        
            for j in self.tag:
                try:
                    self.emission["*U*"][j] = 1
                except KeyError:
                    self.emission["*U*"] = {j:1}

    def build_semantics(self):
        for line in self.sentences:
            #Add the emission matrix for start state
            current_pos = 'ss'
            word_pos = line.split()
            for word in word_pos:
                w = word[0:-3]
                t = word[-2:]
                
                self.add_to_tag(t)

                # Add to the emission matrix
                self.add_to_emission(t,w)

                # Add to the transition matrix
                next_pos = t
                self.add_to_transition(current_pos,next_pos)
                current_pos = next_pos
            #Add the transition matrix for terminal state
            next_pos = 'tt'
            self.add_to_transition(current_pos,next_pos)
        # self.add_unknown()

    def smooth_transition(self):
        self.tag['tt'] = 0
        for i in self.transition:
            try:
                tag_total = self.tag[i]
                for j in self.tag:
                    len_tag = tag_total + len(self.tag)
                    try:
                        self.transition[i][j] = (self.transition[i][j] + 1) / len_tag
                    except KeyError:
                        self.transition[i][j] = 1 / len_tag
            except KeyError:
                continue
        self.tag.pop('tt', None)
        for j in self.tag:
            len_tag = len(self.sentences)
            try:
                self.transition['ss'][j] = self.transition['ss'][j] / len_tag
            except KeyError:
                self.transition['ss'][j] = 1 / len_tag 


    def smooth_emission(self):
        for i in self.emission:
            for j in self.emission[i]:
                self.emission[i][j] = self.emission[i][j] / self.tag[j]
        self.emission['*S*'] = {'ss':1}

    def build_output(self):
        self.output['emission'] = self.emission
        self.output['transition'] = self.transition
        self.output['tag'] = self.tag

    def create_hmm(self):
        self.build_semantics()
        self.smooth_transition()
        self.smooth_emission()
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