# Default word tokens
PAD_token = 0  # Used for padding short sentences
SOS_token = 1  # Start-of-sentence token
EOS_token = 2  # End-of-sentence token

class Voc:
    def __init__(self, name):
        self.name = name
        self.reset()

    def reset(self):
        self.word2index = {}
        self.word2count = {}
        self.index2word = {PAD_token: "PAD", SOS_token: "SOS", EOS_token: "EOS"}
        self.num_words = 3  # Count SOS, EOS, PAD

    def addSentence(self, sentence):
        for word in sentence.split(' '):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.word2count[word] = 1
            self.index2word[self.num_words] = word
            self.num_words += 1
        else:
            self.word2count[word] += 1

    # Remove words below a certain count threshold
    def trim(self, min_count):

        keep_words = []
        for k, v in self.word2count.items():
            if v >= min_count:
                keep_words.append(k)

        print('keep_words {} / {} = {:.4f}'.format(
            len(keep_words), len(self.word2index), len(keep_words) / len(self.word2index)
        ))

        self.reset()
        for word in keep_words:
            self.addWord(word)


import unicodedata
import re
MAX_LENGTH = 10  # Maximum sentence length to consider

# Turn a Unicode string to plain ASCII, thanks to
# https://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters
def normstr(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    return s

def sent_len(sent):
    return len(sent.split(' '))

# Returns True iff both sentences in a pair 'p' are under the MAX_LENGTH threshold
def less_than_max(pair,M=MAX_LENGTH):
    # Input sequences need to preserve the last word for EOS token
    A,B = pair
    return sent_len(A) < M and sent_len(B) < M
    #return len(pair[0].split(' ')) < MAX_LENGTH and len(p[1].split(' ')) < MAX_LENGTH

def loadPrepareData(datafile):
    voc = Voc('data')
    plines = open(datafile, encoding='utf-8').read().strip().split('\n')
    plines= [ l.split('^') for l in plines ]
    plines = [ [normstr(a), normstr(b)] for a,b in plines ]

    for a,b in plines:
        voc.addSentence(a)
        voc.addSentence(b)
    return voc, plines 


# Load/Assemble voc and pairs
import os
#save_dir = os.path.join("data", "save")
voc, plines = loadPrepareData('./data/cornell movie-dialogs corpus/formatted_movie_lines.txt')
# Print some pairs to validate
for p in plines[:10]:
    print(p)
