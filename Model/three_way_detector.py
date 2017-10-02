from collections import deque
from bloom_filter import *
import ahocorasick as ahc
import math


class three_way_detector:
    def __init__(self, patt_file, input_file):
        self.bases = (113, 117, 119, 123, 129, 131, 137)
        self.filter = ff_bloom_filter(10000007)
        self.patt_file = patt_file + ' '
        self.input_file = input_file + ' '
        self.patterns, self.patt_code = [], []
        self.input_phrases,self.input_phrases_idx = [],[]
        self.input_code = deque()
        self.org_set = set()

    def display(self):
        print self.patt_file
        print self.input_file

    def find_patterns(self):
        hold, word, appended = 0, '', True
        window = deque()
        for c in self.patt_file:
            if 'A' <= c <= 'Z':
                appended = False
                hold = hold + ord(c) - 65
                word = word + c
            else:
                if appended is False:
                    self.patt_code.append(hold)
                    window.append(word)
                    if len(window) == 3:
                        self.patterns.append(' '.join(list(window)))
                        window.popleft()
                    hold, word, appended = 0, '', True

                # print self.patt_code
                # print self.patterns
                # print '\n'
                # print self.input_code, '\n', self.input_words

    def roll_hash(self, prev, next, present_hashes):
        next_hash = present_hashes
        for idx, base in enumerate(self.bases):
            next_hash[idx] -= prev
            next_hash[idx] /= base
            next_hash[idx] += next * math.pow(base, 2)
        return next_hash

    def preprocess(self):
        window = deque()
        indices = [0] * 7
        a, b, c = self.patt_code[0], self.patt_code[1], self.patt_code[2]
        for idx, base in enumerate(self.bases):
            indices[idx] = a + b * base + c * math.pow(base, 2)
        self.filter.set_bit(1, indices)
        window.extend([a, b, c])

        for code in self.patt_code[3:]:
            x = window.popleft()
            window.append(code)
            indices = self.roll_hash(x, code, indices)
            self.filter.set_bit(1, indices)

    def scan_corpus(self):
        hold, word, appended, shift_no = 0, '', True, 0
        window = deque()
        indices = [0] * 7
        prev = ''
        first,pair = True,[]
        for idx,c in enumerate(self.input_file):
            if c >= 'A' and c <= 'Z':
                if first:
                    pair.append(idx)
                    first = False
                appended = False
                hold = hold + ord(c) - 65
                word = word + c
            else:
                if appended is False:
                    self.input_code.append(hold)
                    pair.append(idx)
                    window.append([word,pair])
                    if len(self.input_code) == 3:
                        if shift_no == 0:
                            a, b, c = self.input_code[0], self.input_code[1], self.input_code[2]
                            for idx, base in enumerate(self.bases):
                                indices[idx] = a + b * base + c * math.pow(base, 2)
                        else:
                            indices = self.roll_hash(prev, hold, indices)

                        if self.filter.look_up(1, indices):
                            self.filter.set_bit(2, indices)
                            #print window[0][1], window[1][1], window[2][1]
                            self.input_phrases.append(window[0][0]+' '+window[1][0]+' '+window[2][0])
                            self.input_phrases_idx.append([window[0][1][0],window[2][1][1]])

                        prev = self.input_code.popleft()
                        window.popleft()

                        shift_no += 1
                    #print self.input_code
                    hold, word, appended,first,pair = 0, '', True,True,[]

    def filter_patterns(self):
        shift_no = 0
        window = deque()
        indices = [0] * 7
        a, b, c = self.patt_code[0], self.patt_code[1], self.patt_code[2]
        for idx, base in enumerate(self.bases):
            indices[idx] = a + b * base + c * math.pow(base, 2)

        if not self.filter.look_up(2, indices):
            self.patterns[shift_no] = ' '

        window.extend([a, b, c])

        for code in self.patt_code[3:]:
            x = window.popleft()
            window.append(code)
            shift_no += 1
            indices = self.roll_hash(x, code, indices)
            if not self.filter.look_up(2, indices):
                self.patterns[shift_no] = ' '

        self.patterns = filter(lambda x: x != ' ', self.patterns)

    # print self.patterns


    def exact_matching(self):
        keywrds = []
        if len(self.input_phrases) != 0:
            A = ahc.Automaton()
            #print self.input_phrases
            for pattern in self.patterns:
                #print pattern
                A.add_word(pattern, pattern)
            A.make_automaton()
            line = ' '.join(self.input_phrases)
            for idx, x in A.iter(line):
                keywrds.append(x)

        checker = set()
        for i in keywrds:
            checker.add(i)

        idx = 0
        for i in self.input_phrases:
            if i not in checker:
                del self.input_phrases_idx[idx]
                idx -= 1
            idx += 1

        self.input_phrases = keywrds

    def calc_plagiarism(self):
        b,final_list, final_index_list = set(),[],[]
        idx = 0
        for idx,each in enumerate(self.input_phrases_idx):
            if len(final_index_list) != 0:
                if final_index_list[len(final_index_list)-1][1] > each[0]:
                    final_index_list[len(final_index_list)-1][1] = each[1]
                    final_list.append(self.input_phrases[idx].split()[2])
                else:
                    final_index_list.append(each)
                    for x in self.input_phrases[idx].split():
                        final_list.append(x)
            else:
                for x in self.input_phrases[idx].split():
                    final_list.append(x)
                final_index_list.append(each)

        #print final_index_list, final_list
        return final_index_list, final_list

    def execute(self):
        self.find_patterns()
        self.preprocess()
        self.scan_corpus()
        self.filter_patterns()
        self.exact_matching()
        return self.calc_plagiarism()
