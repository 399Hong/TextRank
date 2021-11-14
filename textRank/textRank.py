
import numpy as numpy
from numpy import dot
from numpy.linalg import norm

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import string
import nltk
import ssl
import sys

import util


class textRank:
    def __init__(self):
        # original text without processing
        self.__originalCorpus = None 
        # original text splited into an list of sentence
        self.__tokenizedSents = None
        # processed sentences in a list
        self.__cleanedSents = None
        # glove wordEmbeddings
        self.__wordEmbeddings = dict()
        self.__sentenceVector = list()
        self.__simlarityMatrix = None
        self.__textRankVector = None
        self.rankedSents = list()
        self.__vectorSize = 0
        

    @property
    def originalCorpus(self) -> str:

        return self.__originalCorpus
    @originalCorpus.setter
    def originalCorpus(self,text : str):
        self.__originalCorpus = text

    @property
    def tokenizedSents(self) -> list :
        return self.__tokenizedSents

    @tokenizedSents.setter
    def tokenizedSents(self, sents : list ):
        self.__tokenizedSents = sents



    @property
    def cleanedSents(self) -> list :
        return self.__cleanedSents
    @cleanedSents.setter
    def cleanedSents(self, sents: list):
        self.__cleanedSents = sents

    def tokenizeSents(self, text: str):
        self.tokenizedSents = util.tokenizeSentences(text)

    def lazySetup(self):
        self.installStopWords()
        self.glove()
    def lazyLoad(self):
        self.preprocessing()
        self.sentences_to_vectors()
        self.vec_to_sim_mat()
        self.text_rank()
        self.generateSentences()

    def readText(self,fileName:str):
        try:
            with open(fileName,mode='r',encoding= 'unicode_escape') as f:
                self.originalCorpus = f.read()
        except:
            print(f"Unable to open and read {filename}. Please check for the existence of the file" )


    def installStopWords(self):
        """
        This function should only be execute once to install stopwords.
        """
        # handle nltk download error
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        nltk.download("stopword")
        nltk.download('punkt')
        nltk.download('wordnet')
    def preprocessing(self):
        # set of stop words such as "the,he,have"
        stop = set(stopwords.words('english'))

        # set of punctuation
        exclude = set(string.punctuation)


        # convert a word to its base form,was→is, dogs→dog
        lemma = WordNetLemmatizer()


        # Replace non-ASCII characters
        def rem_ascii(s):
            return "".join([c for c in s if ord(c) < 128])


        # Cleaning the text sentences so that punctuation marks, stop words and digits are removed.
        def clean(word):
            stopPuncFree = word if (word not in stop) and (word not in exclude) else ""
            # remove digit
            processed = re.sub(r"\d+", "", stopPuncFree)
            return processed

        #split text into sentences
        self.tokenizeSents(self.originalCorpus)

        # Split the sentence into words
        cleaned_sents = []
        for s in self.tokenizedSents:
            words = word_tokenize(s)
            # clean non-ascii, punctuation stop word and digits.
            cleaned_sents.append( ' '.join(filter(None,[lemma.lemmatize(rem_ascii(clean(w))).strip()for w in words])))
        self.cleanedSents = cleaned_sents     

    def glove(self, fileName:str = "glove.6B.200d.txt"):
    
        self.__vectorSize = int(fileName.split('.')[-2][0:-1])
        
        with open(fileName, encoding='utf-8') as f:
            for line in f:
                values = line.split()
                word = values[0]
                coefs = numpy.asarray(values[1:], dtype='float32')
                self.__wordEmbeddings[word] = coefs
        
    def sentences_to_vectors(self):

        for sentence in self.cleanedSents:
            if len(sentence) != 0:
                vector = sum([self.__wordEmbeddings.get(w, numpy.zeros((self.__vectorSize,))) for w in sentence.split()]) / (
                        len(sentence.split()) + 0.001)
            else:
                vector = numpy.zeros((self.__vectorSize,))
            self.__sentenceVector.append(vector)

    def vec_to_sim_mat(self, ):

        def cosine_sim(a, b):
            c = b.reshape(self.__vectorSize,1)
            return dot(a,c) / (norm(a) * norm(b))

        size = len(self.__sentenceVector)
        self.__simlarityMatrix = numpy.zeros([size,size])

        for i in range(size):
            for j in range(size):
                if i != j:
                    self.__simlarityMatrix[i][j] = cosine_sim(self.__sentenceVector[i].reshape(1,self.__vectorSize), self.__sentenceVector[j].reshape(1,self.__vectorSize))[0,0]
    
    def text_rank(self, damping=0.85, max_steps=100, min_diff=1e-5):
        self.__textRankVector = numpy.array([1 for x in range(len(self.__simlarityMatrix))])

        previous_vector = 0

        for step in range(max_steps):
            self.__textRankVector = (1 - damping) + damping * numpy.matmul(self.__simlarityMatrix, self.__textRankVector)
            if abs(previous_vector - sum(self.__textRankVector)) < min_diff:
                break
            else:
                previous_vector = sum(self.__textRankVector)
    def generateSentences(self):
        
        if self.__textRankVector.all() != None:
            sorted_vector = numpy.argsort(self.__textRankVector)
            sorted_vector = list(sorted_vector)
            sorted_vector.reverse()

            count = 0
            for step in range(len(self.__textRankVector)):
                sentence = self.__tokenizedSents[sorted_vector[count]]
                sentence = " ".join(sentence.split())
                self.rankedSents.append(sentence)
                count += 1
    def displaySents(self, number:int = 5):
        size = len(self.rankedSents)
        if size < number:
            print()
            print(f"There are insufficent setences to display. Displaying {size} sentences in total.")
            print()
            for i in range(size):
                print(i+1, self.rankedSents[i])
        else:
            print()
            print(f"Display top {number} sentences....")
            print()
            for i in range(number):
                print(i+1,self.rankedSents[i])
                print()
    def getSents(self,number:int = 7) -> list:
        size = len(self.rankedSents)
        if size < number:
            return [i.strip() for i in self.rankedSents]
        else:
             return [i.strip() for i in self.rankedSents[0:number+1]]
    def reset(self):
        self.__originalCorpus = None 
        # original text splited into an list of sentence
        self.__tokenizedSents = None
        # processed sentences in a list
        self.__cleanedSents = None
        # glove wordEmbeddings
        #self.__wordEmbeddings = dict()
        self.__sentenceVector = list()
        self.__simlarityMatrix = None
        self.__textRankVector = None
        self.rankedSents = list()

