import numpy 
import os
import re
import sys
import platform

def translate_non_alphanumerics(to_translate, translate_to=u' '):
    not_letters_or_digits = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~1234567890$&\u201C\u2018\u2019\u2014\u201D\u00AB.\u20AC\u25A0\uFD3E\uFD3F\u2022\u2013\u060C\u061F\u00BB\u0640\u2026\u202B\u2022\u202B\u200F\u200F\u200E\u200E\u200E\u200E'
    translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)
    return to_translate.translate(translate_table)


def count_word(text_file_path):
    text_file= open(text_file_path)
    document = text_file.read()
    if document == "":
       return 0
   

    words = re.split(ur"[\s,]+",re.sub(ur"\p{P}+", "",document),flags=re.UNICODE)
    return len(words)

def compute_off_topic(old_uri_id,file_list,timemap_dict,count_list,off_topic_count_file,threshold):
    if len(count_list) == 0 or max(count_list)==0:
        return
    if count_list[0]==0:
        print old_uri_id
        return
    
    percentage_list = [(count_list[i] - count_list[0]+0.0) / count_list[0] for i in range(len(count_list))]
    for  idx,p in enumerate(percentage_list):
        if p < threshold:
            memento_uri = timemap_dict[str(old_uri_id)][str(file_list[idx])]
            off_topic_count_file.write( str(p)+"\t"+memento_uri+"\n")                    

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
    

def get_off_topic_memento(timemap_file_name,off_topic_count_file, collection_directory,threshold):

  timemap_dict = convert_timemap_to_hash(timemap_file_name)

  timemap_list_file = open(timemap_file_name)
  print "Detecting off-topic mementos using Word Count method."
  off_topic_count_file.write( "Similarity\tmemento_uri\n") 
  count_list = []
  file_list = []
  old_uri_id = "0"
  old_mem_id = 0

  for memento_record in timemap_list_file:
    fields = memento_record.split("\t")
    uri_id = fields[0]
    dt = fields[1]
    mem_id = fields[2]
    uri = fields[3]
    
    if old_uri_id != uri_id and old_uri_id > -1:
          compute_off_topic(old_uri_id,file_list,timemap_dict,count_list,off_topic_count_file,threshold)
          
          count_list = []
          file_list = []
      
    text_file_path = collection_directory+"/text/"+uri_id+"/"+dt+".txt"
    if os.path.exists(text_file_path):
        file_list.append(dt)
        word_count = count_word(text_file_path)
        count_list.append(word_count)
      
    old_uri_id = uri_id      
  compute_off_topic(old_uri_id,file_list,timemap_dict,count_list,off_topic_count_file,threshold)
  