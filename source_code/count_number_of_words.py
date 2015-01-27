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

def print_the_list_t0(old_uri_id, count_file, count_list, percentage_file, cumulative_file):
    if len(count_list) == 0 or max(count_list)==0:
        return
    if count_list[0]==0:
        print old_uri_id
        return
    
    count_file.write(old_uri_id)

    for c in count_list:
        count_file.write("\t"+str(int( (c*100.0)/count_list[0])))
    count_file.write("\n")
    
    percentage_list = [count_list[i]*100 / count_list[0] for i in range(len(count_list))]
     
    hist_tuple = numpy.histogram( percentage_list,bins=[-1,6,11, 16, 21, 26, 31, 36, 41, 46, 51,56,61,66,71,76,81,86,91,96,101,10000])
    hist_list = hist_tuple[0]
    #print percentage_list
    percentage_file.write((old_uri_id+"\t"+ str(hist_list).replace("[","").replace("]","").replace("  "," ").replace(" ","\t")+"\n").replace("\t\t","\t"))
    cum_list = numpy.cumsum(hist_list)
  #  print hist_list
    cumulative_file.write((old_uri_id+"\t"+ str(cum_list).replace("[","").replace("]","").replace("  "," ").replace(" ","\t")+"\n").replace("\t\t","\t"))

    
   
def print_the_list_prev(old_uri_id, count_file, count_list, percentage_file, cumulative_file):
    if len(count_list) == 0 or max(count_list)==0:
        return
    if count_list[0]==0:
        print old_uri_id
        return
    
    count_file.write(old_uri_id)

    percentage_list =[]
    for idx, c in enumerate(count_list):
        
        if idx == 0:
            prev_c =  c
            continue
        
        if prev_c >0:
            count_file.write("\t"+str(int( (c*100.0)/prev_c)))
            percentage_list.append( int( (c*100.0)/prev_c))
        else:
            count_file.write("\t1000")
            percentage_list.append(  1000)

        prev_c = c
    count_file.write("\n")
    
     
    hist_tuple = numpy.histogram( percentage_list,bins=[-1,6,11, 16, 21, 26, 31, 36, 41, 46, 51,56,61,66,71,76,81,86,91,96,101,10000])
    hist_list = hist_tuple[0]
    #print percentage_list
    percentage_file.write((old_uri_id+"\t"+ str(hist_list).replace("[","").replace("]","").replace("  "," ").replace(" ","\t")+"\n").replace("\t\t","\t"))
    cum_list = numpy.cumsum(hist_list)
  #  print hist_list
    cumulative_file.write((old_uri_id+"\t"+ str(cum_list).replace("[","").replace("]","").replace("  "," ").replace(" ","\t")+"\n").replace("\t\t","\t"))

    
    
    
if __name__ == "__main__":
       if len(sys.argv) > 1:
          collection_id = sys.argv[1]
       else:
          collection_id = "1068"
          
       if platform.system().startswith("Windows")  :
          input_base_dir = "C:/Users/yasmin/Desktop/data_files/collection_"+collection_id
          output_base_dir= "c:/dropbox/Dropbox/Coding/Data_files/collection_"+collection_id
       else:
          input_base_dir = "/Users/yasmin/Desktop/data_files/collection_"+collection_id
          output_base_dir= "/Users/yasmin/Dropbox/Coding/Data_files/collection_"+collection_id
      
       
       timemap_list_file=open(output_base_dir+"/timemap.txt")
       count_word_directory = output_base_dir+"/count_word/"
       if not os.path.exists(count_word_directory):
           os.makedirs(count_word_directory)

       count_file= open(count_word_directory+"/count_words.txt","w")
       
       count_file_t0 = open(count_word_directory+"/count_file_t0.txt","w")
       percentage_file_t0= open(count_word_directory+"/percentage_file_t0.txt","w")
       cumulative_file_t0= open(count_word_directory+"/cumulative_file_t0.txt","w")

       count_file_prev = open(count_word_directory+"/count_file_prev.txt","w")
       percentage_file_prev= open(count_word_directory+"/percentage_file_prev.txt","w")
       cumulative_file_prev= open(count_word_directory+"/cumulative_file_prev.txt","w")
       
       cumulative_file_t0.write("id\t5\t10\t15\t20\t25\t30\t35\t40\t45\t50\t55\t60\t65\t70\t75\t80\t85\t90\t95\t100\t10000\n")
       percentage_file_t0.write("id\t5\t10\t15\t20\t25\t30\t35\t40\t45\t50\t55\t60\t65\t70\t75\t80\t85\t90\t95\t100\t10000\n")
       
       cumulative_file_prev.write("id\t5\t10\t15\t20\t25\t30\t35\t40\t45\t50\t55\t60\t65\t70\t75\t80\t85\t90\t95\t100\t10000\n")
       percentage_file_prev.write("id\t5\t10\t15\t20\t25\t30\t35\t40\t45\t50\t55\t60\t65\t70\t75\t80\t85\t90\t95\t100\t10000\n")
 
       last_memento_dt = "-1"
       old_uri_id = "-1"
       count_list=[]
       for memento_record in timemap_list_file:
           
           fields = memento_record.split("\t")

           uri_id = fields[0]
           dt = fields[2]
           mem_id = int(fields[3])

           
           if old_uri_id != uri_id and old_uri_id > -1:
               print_the_list_t0(old_uri_id, count_file_t0, count_list,percentage_file_t0, cumulative_file_t0) 
               print_the_list_prev(old_uri_id, count_file_prev, count_list,percentage_file_prev, cumulative_file_prev) 
               count_list = []
           
           text_file_path = input_base_dir+"/text/"+uri_id+"/"+dt+".txt"
           if os.path.exists(text_file_path):
               word_count = count_word(text_file_path)
               count_list.append(word_count)
               count_file.write(uri_id+"\t"+dt+"\t"+str(word_count)+"\n")
           
           old_uri_id = uri_id      

