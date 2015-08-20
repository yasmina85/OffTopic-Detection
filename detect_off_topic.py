from bs4 import BeautifulSoup
import urllib2
import re
import sys
import os
sys.path.append("source_code")
import seed_extractor
import timemap_downloader
import argparse
import random
import html_wayback_downloader
import off_topic_detector_cos_sim
import off_topic_detector_count_words
import urlparse
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
        


parser = argparse.ArgumentParser(description='Detecting off-topic webpages.')


parser.add_argument('-d', dest='dir', 
                   help='The directory that is used for the downloaded/processed data')
                   
parser.add_argument('-th', dest='threshold', 
                   help='The threshold to compute the off-topic pages between 0 to 1. The default threshold is 0.15')
                
parser.add_argument('-o', dest='file', 
                   help='The file path to write the output')

parser.add_argument('-t', dest='timemap_uri', 
                   help='The link of a timemap (it should be in timemap/link format)')

parser.add_argument('-i', dest='id', 
                   help='The collection id as appeared on archive-it')

parser.add_argument('-r', dest='uri', 
                   help='The collection uri as appeared on archive-it')

parser.add_argument('-m', dest='mode', default="cosim",
                   help='The similarity measure: cosim or wcount. The default is cosim.')
                   
args = parser.parse_args()

data_directory = 'tmp'
if args.dir != None:
   data_directory =  args.dir
   
threshold = 0.15
if args.threshold != None:
   threshold =  float(args.threshold)

output_file = sys.stdout
if args.file != None:
    output_file = open(args.file,'w')

if args.mode != None:
    mode = args.mode 
    
    if mode != "cosim" and mode != "wcount":
         parser.print_help()
         sys.exit(1)
         
base_timemap_link_uri = "http://wayback.archive-it.org/"
if args.id !=None:
    # extract from id
    collection_id = args.id
    collection_directory = data_directory+"/collection_"+str(collection_id)
    seed_extractor.seed_extractor_from_id(collection_id,collection_directory)
    seed_list_file = collection_directory+"/seed_list.txt"
    timemap_file_name = collection_directory+"/timemap.txt"
    timemap_downloader.download(seed_list_file, base_timemap_link_uri+ str(collection_id)+"/timemap/link", collection_directory)
    
elif args.uri !=None:
    # extract from uri
    collection_uri = args.uri
    o = urlparse.urlparse(args.uri)
    collection_id = o.path.split('/')[-1]
    if collection_id == "":
        collection_id = o.path.split('/')[-2]
        
    collection_directory = data_directory+"/collection_"+str(collection_id)
    seed_list_file = collection_directory+"/seed_list.txt"
    timemap_file_name = collection_directory+"/timemap.txt"
    
    seed_extractor.seed_extractor_from_uri(collection_uri,collection_directory)
    timemap_downloader.download(seed_list_file, base_timemap_link_uri+str(collection_id)+"/timemap/link", collection_directory)
elif args.timemap_uri !=None:
    # extract directly from timemap
    memento_list = timemap_downloader.get_mementos_from_timemap(args.timemap_uri)
    collection_id = str(random.randrange(1000000))
    collection_directory = data_directory+"/collection_"+collection_id
    timemap_file_name =collection_directory+"/timemap.txt"
    ensure_dir(timemap_file_name)
    timemap_file =  open(timemap_file_name,'w')
    timemap_downloader.write_timemap_to_file(1, memento_list,timemap_file) 
else:
    parser.print_help() 

html_wayback_downloader.download_html_from_wayback(timemap_file_name,collection_directory)      
os.system('./extract_text_from_html '+timemap_file_name+' '+  collection_directory)

if mode == "cosim" :
    off_topic_detector_cos_sim.get_off_topic_memento(timemap_file_name,output_file,collection_directory,threshold)
elif mode ==  "wcount":
    off_topic_detector_count_words.get_off_topic_memento(timemap_file_name,output_file,collection_directory,threshold)
else:
    print "Undefined methods"


