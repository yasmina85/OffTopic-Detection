from bs4 import BeautifulSoup
import urllib2
import re
import sys
import os

if __name__ == "__main__":
        if len(sys.argv) > 1:
            collection_id = sys.argv[1]
        else:
         print "\nUsage get_off_topic_using_cosine_similarity [collection_id]"
         print "collection_id: is the id of the collection as it appears on ArchiveIt"
         sys.exit(1)
 
        collection_uri = "https://archive-it.org/collections/"+str(collection_id)+"/?page="
        collection_directory = "data/collection_"+str(collection_id)
        if not os.path.exists(collection_directory):
            os.makedirs(collection_directory)
            
        seed_file = open( collection_directory+"/seed_list.txt","w")
        id = 0
        for i in range(1,20):
            page_uri = collection_uri + str(i)
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
        print str(id)+" URIs are extracted from collection "+str(collection_id)
        seed_file.close()
