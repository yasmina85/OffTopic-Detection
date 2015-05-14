from bs4 import BeautifulSoup
import urllib2
import re
import sys
import os

def seed_extractor_from_uri(collection_uri,collection_directory):
        if not os.path.exists(collection_directory):
            os.makedirs(collection_directory)
            
        seed_file = open( collection_directory+"/seed_list.txt","w")
        id = 0
        for i in range(1,20):
            page_uri = collection_uri +"/?page="+str(i)
            request = urllib2.Request(page_uri)
            opener = urllib2.build_opener()
            response = opener.open(request)
    
            the_page = response.read()
            response.close();
    
            soup = BeautifulSoup(the_page)
    
            links = soup.findAll('h3',attrs={"class":"url"})
            for link in links:
                if link.a != None:
                    seed_uri = link.a.get('title').encode("utf-8")
                    if seed_uri.endswith(".png") or  seed_uri.endswith(".jpg") or  seed_uri.endswith(".pdf") or  seed_uri.endswith(".jpeg"):
                        continue;
                    else:
                        id = id + 1
                        print link.a.get('title').encode("utf-8")
                        seed_file.write(str(id)+"\t"+ link.a.get('title').encode("utf-8") +"\n")
        print str(id)+" URIs are extracted from collection "+str(collection_uri)
        seed_file.close()


def seed_extractor_from_id(collection_id,data_directory):
        collection_uri = "https://archive-it.org/collections/"+str(collection_id)
        seed_extractor_from_uri(collection_uri,data_directory)