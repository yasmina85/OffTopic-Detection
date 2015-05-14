
# Prerequisite
* Python 2.7+ https://www.python.org/downloads/
* Install NLTK http://www.nltk.org/install.html
* Install scikit-learn http://scikit-learn.org/dev/install.html
* java 1.7+

## For Mac OS/UNIX OS
To setup the environment 

  ```
  git clone https://github.com/yasmina85/OffTopic-Detection.git
  cd OffTopic-Detection
  sudo pip install -r requirements.txt
  python setup.py
  ```

##To detect the off-topic for a collection
* Using collection id from Archive-It
  
  ```python detect_off_topic.py -i [collection_id]```
  
  For example:
   
  ```python detect_off_topic.py -i 1860```
  
* Using collection uri from Archive-It

  ```python detect_off_topic.py -r [collection_uri]```
  
  For example:
   
  ```python detect_off_topic.py -r https://www.archive-it.org/collections/1860```
  
* To check off-topic for one timemap

  ```python detect_off_topic.py -t [timemap_uri]```
  
  For example:
   
  ```python detect_off_topic.py -t https://www.archive-it.org/collections/1860```

* The default will list the off-topic mementos on the screen, if you want to forward the result to another file

  ```python detect_off_topic.py -i [collection_id] -o [filename]```

* To change the threshold value

  ```python detect_off_topic.py -i [collection_id] -th 0.2```

* To change the directory that is used to download/process the data

  ```python detect_off_topic.py -i [collection_id] -data [directory]```
  
## Feedback
Your feedback is always welcome. You can send me an email on yasmin@cs.odu.edu or open an issue on github.