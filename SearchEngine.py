# -*- coding: utf-8 -*-
"""
Name: Vaibhav Murkute
Project: Document Search Engine
"""

import os
import math
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

corpus = {}
postings_list = {}
sorted_weights = {}
num_docs = 0;
docs_dir = './presidential-debates'
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def Main():
    global num_docs
    global corpus
    global postings_list
    num_docs = 0
    if(os.path.isdir(docs_dir)):
        for file_name in os.listdir(docs_dir):
            num_docs += 1
            doc_count = Counter()
            file = open(os.path.join(docs_dir,file_name), "r", encoding="UTF-8")
            doc = file.read()
            file.close()
            doc = doc.lower()
            doc = tokenizer.tokenize(doc)
            doc = remove_stopWords(doc)
            
            for token in doc:
                doc_count[token] += 1
                if token in corpus:
                    corpus[token][file_name] = doc_count[token]
                    postings_list[token][file_name] = getweight(file_name, token)
                else:
                    corpus[token] = {}
                    corpus[token][file_name] = doc_count[token]
                    postings_list[token] = {}
                    postings_list[token][file_name] = getweight(file_name, token)
    
    print("IDF(agenda):",getidf("agenda"))
    print("getweight(2012-10-03.txt, health): %.12f" % getweight("2012-10-03.txt","health"))
    print("query(terror attack):",query("terror attack"))
    

def remove_stopWords(doc):
    result = []
    for word in doc:
        if word not in stop_words:
            result.append(stemmer.stem(word))
    return result

def getidf(token):
    idf=0
    if token in corpus:
        dft = len(corpus[token])
        idf = math.log10((num_docs/dft))
        return idf
    else:
        return -1

def gettf(freq):
    return (1+math.log10(freq))

def getweight(filename, token):
    if filename in corpus[token].keys():
        return (gettf(corpus[token][filename]) * getidf(token))
    else:
        return 0
    
def filterinput(input):
    output = input.lower()
    output = tokenizer.tokenize(output)
    output = remove_stopWords(output)
    return output

def query(qstring):
    result = []
    qstring = filterinput(qstring)
    counter = Counter()
    query_weight = {}
    result_doclist = {}
    norm_doclist = {}
    
    for word in qstring:
        counter[word] += 1
        query_weight[word] = gettf(counter[word])
        if word in postings_list:
            for doc in postings_list[word].keys():
                if doc not in result_doclist:
                    result_doclist[doc] = (postings_list[word][doc] * query_weight[word])
                    norm_doclist[doc] = postings_list[word][doc]**2
                else:
                    result_doclist[doc] += (postings_list[word][doc] * query_weight[word])
                    norm_doclist[doc] += postings_list[word][doc]**2
    
    for doc in result_doclist:
        if norm_doclist[doc] != 0:
            result_doclist[doc] = result_doclist[doc] / math.sqrt(norm_doclist[doc])
    
    if not result_doclist:
        return ["None",0]
    else:
        matched_doc = max(result_doclist, key=result_doclist.get)
        result.append(matched_doc)
        result.append(result_doclist[matched_doc])
        return result
    
  
def sortdictionary(postings_list):
    global sorted_weights
    for token in postings_list:
        values = postings_list[token].values()
        values.sort(reverse=True)
        sorted_weights[token] = values
        
    
if __name__ == '__main__':
    Main()
                 
                
    
