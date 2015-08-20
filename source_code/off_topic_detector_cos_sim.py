import os
from sets import Set
import nltk
import string
from sklearn.metrics.pairwise import cosine_similarity
import ntpath
import sys
import platform
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()
def load_stopwords():
    f = open('stopwords.txt')
    stopwords =[]
    for w in f:
        stopwords.append(w.replace('\r','').replace('\n',''))
    return stopwords

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems


def build_vector_from_file_list(file_list):
    text_dictionary = {}

    for text_file in file_list:
        shakes = open(text_file, 'r')
        text = shakes.read()
        if len(text)==0:
            continue
        lowers = text.decode('utf-8', errors='ignore').lower()
    
        no_punctuation = string.translate(lowers, string.punctuation)
        text_dictionary[text_file] = no_punctuation
    return text_dictionary

def build_vector_from_file(text_file):
    text_dictionary = {}

    shakes = open(text_file, 'r')
    text = shakes.read()
    if len(text)==0:
        return
    lowers = text.decode('utf-8', errors='ignore').lower()

    no_punctuation = string.translate(lowers, string.punctuation)
    text_dictionary[text_file] = no_punctuation
    return text_dictionary


def convert_timemap_to_hash(timemap_file_name):
    timemap_list_file = open(timemap_file_name)
    timemap_dict = {}
    for memento_record in timemap_list_file:
        fields = memento_record.split("\t")
        uri_id = fields[0]
        dt = fields[1]
        uri = fields[3]
        if not(uri_id in timemap_dict):
              timemap_dict[uri_id]={}
        timemap_dict[uri_id][dt]=uri
    timemap_list_file.close()
    return timemap_dict
    
def compute_off_topic(old_uri_id,file_list,timemap_dict,off_topic_cosine_file,tfidf,threshold):
    memento_t0 = ntpath.basename(file_list[0].replace('.txt',''))
    vector_text = build_vector_from_file_list(file_list)
    if vector_text is not None  and len(vector_text)>0 :
        tfidf_matrix = tfidf.fit_transform(vector_text.values())
        
        first_index = -1
        for j in enumerate(tfidf_matrix.toarray()):
            if vector_text.keys()[j[0]]==file_list[0]:
                first_index=j[0]
        cosine_similarity_results_matrix = cosine_similarity(tfidf_matrix[first_index], tfidf_matrix)
        computed_file_list = []

        for  document_list in enumerate(tfidf_matrix.toarray()):
            file_name =  vector_text.keys()[document_list[0]]
            computed_file_list.append( ntpath.basename(file_name.replace('.txt','')))
        for train_row in cosine_similarity_results_matrix:
            for idx, test_cell in enumerate(train_row):
                if test_cell < threshold:
                    memento_uri = timemap_dict[str(old_uri_id)][str(computed_file_list[idx])]
                    off_topic_cosine_file.write( str(test_cell)+"\t"+memento_uri+"\n")                    
    

   
def get_off_topic_memento(timemap_file_name,off_topic_cosine_file, collection_directory,threshold):
         
    english_stopwords = load_stopwords()
    timemap_dict = convert_timemap_to_hash(timemap_file_name)
    
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    old_uri_id = "0"
    old_mem_id = 0
    file_list=[]

    timemap_list_file = open(timemap_file_name)
    print "Detecting off-topic mementos using Cosine Similarity method."
    off_topic_cosine_file.write( "Similarity\tmemento_uri\n") 
    for memento_record in timemap_list_file:
          fields = memento_record.split("\t")
          uri_id = fields[0]
          dt = fields[1]
          mem_id = fields[2]
          uri = fields[3]

          text_file = collection_directory+"/text/"+uri_id+"/"+dt+".txt"
          if not os.path.isfile(text_file):
              continue
          
          if old_uri_id != uri_id and len(file_list)>0:
              compute_off_topic(old_uri_id,file_list,timemap_dict,off_topic_cosine_file,tfidf,threshold)
              file_list=[]
          file_list.append(text_file)
          old_uri_id=uri_id

            
    if len(file_list)>0:
        compute_off_topic(uri_id,file_list,timemap_dict,off_topic_cosine_file,tfidf,threshold)

