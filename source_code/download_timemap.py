import re
import urllib2
from sys import argv
import sys
import time
from urlparse import urlparse


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
        

if __name__ == "__main__":
    if len(sys.argv) > 1:
         collection_id = sys.argv[1]
    else:
         print "\nUsage get_off_topic_using_cosine_similarity [collection_id]"
         print "collection_id: is the id of the collection as it appears on ArchiveIt"
         sys.exit(1)
    collection_directory = "data/collection_"+str(collection_id)
    
    seed_list_file = open(collection_directory+"/seed_list.txt")
    w=open(collection_directory+"/timemap.txt","w")

    orginalExpression = re.compile( r"<http://[A-Za-z0-9.:=/%-_ ]*>; [\s]*rel=\"original\"," )
    mementoExpression = re.compile( r"(<http://[A-Za-z0-9.:=/&,%-_ \?]*>;\s?rel=\"(memento|first memento|last memento|first memento last memento|first last memento)\";\s?datetime=\"(Sat|Sun|Mon|Tue|Wed|Thu|Fri), \d{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (19|20)\d\d \d\d:\d\d:\d\d GMT\")" )
    zeroMementoExpression = re.compile(r"Resource: http://[A-Za-z0-9.:=/&,%-_ ]*")

    baseuri="https://wayback.archive-it.org/"+collection_id+"/timemap/link/"

    for line in seed_list_file:
        seed_record = line.split("\t")
        id = seed_record[0]
        uri = seed_record[1]
        hostname = urlparse(uri).hostname
        
        try:
            print "Downloading timemap using uri "+uri
            request = urllib2.Request(baseuri+uri)
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
                memdt = memUri[36:50]
                

                w.write( str(id)+"\t"+memdt+"\t"+str(count)+"\t"+memUri[1 : len(memUri)-1]+"\n")
            w.flush()
        except urllib2.HTTPError, e:
            print "Timemap is not available "+str(e.code) +"\t"+str(e.msg)+"\n"
        except urllib2.URLError, e:
            print "Timemap is not available "+str(e.args)+"\t"+str(e.reason)+"\n"

    w.close()


