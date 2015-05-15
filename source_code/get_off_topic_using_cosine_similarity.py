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


   
if __name__ == "__main__":
   if len(sys.argv) > 2:
         collection_id = sys.argv[1]
         threshold = float(sys.argv[2])
   else:
         print "\nUsage get_off_topic_using_cosine_similarity [collection_id] [threshold]"
         print "collection_id: is the id of the collection as it appears on ArchiveIt"
         print "threshold: is the threshold for cosine similarity ranges from 0-1.0, suggested value is 0.15\n"
         sys.exit(1)
         
   collection_directory = "data/collection_"+str(collection_id)
   off_topic_cosine_file=open(   collection_directory+"/off_topic_cosine_file.txt",'w')
      
   timemap_list_file=open(collection_directory+"/timemap.txt")
   english_stopwords = load_stopwords()
   
   tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
   old_uri_id = "0"
   old_mem_id = 0
   file_list=[]
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
            print "Detecting off-topic for uri with id: "+old_uri_id
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
                            off_topic_cosine_file.write( old_uri_id+"\t"+str(test_cell)+"\t"+computed_file_list[idx]+"\n")                    
            old_uri_id=uri_id
            file_list=[]
            file_list.append(text_file)

          else:
            file_list.append(text_file)


