import re
import urllib2
from sys import argv
import sys
import time
from urlparse import urlparse

orginalExpression = re.compile( r"<http://[A-Za-z0-9.:=/%-_ ]*>; [\s]*rel=\"original\"," )
mementoExpression = re.compile( r"(<http://[A-Za-z0-9.:=/&,%-_ \?]*>;\s?rel=\"(memento|first memento|last memento|first memento last memento|first last memento)\";\s?datetime=\"(Sat|Sun|Mon|Tue|Wed|Thu|Fri), \d{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (19|20)\d\d \d\d:\d\d:\d\d GMT\")" )
zeroMementoExpression = re.compile(r"Resource: http://[A-Za-z0-9.:=/&,%-_ ]*")

def download(seed_list_file_name, base_timemap_link_uri , collection_directory):
    timemap_file=open(collection_directory+"/timemap.txt","w")
    seed_list_file = open(seed_list_file_name)


    for line in seed_list_file:
        seed_record = line.split("\t")
        id = seed_record[0]
        uri = seed_record[1]
        hostname = urlparse(uri).hostname
        
        print "Downloading timemap using uri "+base_timemap_link_uri+"/"+uri
        memento_list = get_mementos_from_timemap(base_timemap_link_uri+"/"+uri)
        
        write_timemap_to_file(id,memento_list,timemap_file)   
    timemap_file.close()
    
def write_timemap_to_file(id, memento_list,timemap_file) :       
        count = 1
        for memento in memento_list:
            timemap_file.write( str(id)+"\t"+memento[0]+"\t"+str(count)+"\t"+memento[1]+"\n")
            timemap_file.flush()
            count = count + 1
    
def get_mementos_from_timemap(base_timemap_link):
        memento_list = []
        try:
            request = urllib2.Request(base_timemap_link)
            opener = urllib2.build_opener()
            response = opener.open(request)

            the_page = response.read()
            response.close();
            count = 0

            list =re.findall(mementoExpression,the_page)
            for mem in list:
                count = count+1
                list = mem[0].split(';')
                memUri= list[0]
                m = re.search('\d{14}', memUri)
                memdt = memUri[36:50]
                if m != None:
                    memdt = m.group(0)
                    memento_list.append( (memdt,memUri[1 : len(memUri)-1]))
        except urllib2.HTTPError, e:
                    print "Timemap is not available "+str(e.code) +"\t"+str(e.msg)+"\n"
        except urllib2.URLError, e:
                    print "Timemap is not available "+str(e.args)+"\t"+str(e.reason)+"\n"
        return memento_list
                
