import re
import urllib2
from sys import argv
import sys
import time
import os

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
        
def download_html_from_wayback( timemap_file_name,collection_directory ) :   
    timemap_file=open(timemap_file_name)
    
    number_of_mementos = 0
    for memento_record in timemap_file:
        number_of_mementos = number_of_mementos + 1
    timemap_file.close()
    
    timemap_file=open(timemap_file_name)
    old_uri_id=""
    number_of_downloading_mementos = 0
    memento_list=[]
    for memento_record in timemap_file:

        fields = memento_record.split("\t")
        uri_id = fields[0]
        dt = fields[1]
        uri = fields[3]
        
        if uri_id != old_uri_id:
            download_memento_list(old_uri_id, memento_list, collection_directory)
            number_of_downloading_mementos=number_of_downloading_mementos+len(memento_list)
            print "Downloading "+str(number_of_downloading_mementos)+" mementos out of "+str(number_of_mementos)
            memento_list=[]
        old_uri_id = uri_id
        memento_list.append( (dt,uri) )
       # time.sleep(2)
    download_memento_list(uri_id, memento_list, collection_directory)
    number_of_downloading_mementos=number_of_downloading_mementos+len(memento_list)
    print "Downloading "+str(number_of_downloading_mementos)+" mementos out of "+str(number_of_mementos)
 
def download_memento_list(uri_id, memento_list, collection_directory):
        if memento_list==[]:
            return
        
        ensure_dir(collection_directory+"/html/"+uri_id+"/")
        for memento in memento_list:
            the_page = get_one_memento(memento[0], memento[1])
            f = open(collection_directory+"/html/"+uri_id+"/"+memento[0]+".html","w")
            f.write(the_page)
            f.close()                
            
def get_one_memento(dt, uri):
        the_page = ""

        uri = uri.replace(dt,dt+"id_")
        try:
            request = urllib2.Request(uri)
            opener = urllib2.build_opener()
            response = opener.open(request)

            the_page = response.read()
            response.close();
            
        except urllib2.HTTPError, e:    
            print uri
            print str(e.code) +"\n"+str(e.msg)+"\n"+str(e.args)
        except urllib2.URLError, e:
            print uri
            print str(e.args)+"\n"+str(e.reason)+"\n"+str(e.args)
        return the_page
            