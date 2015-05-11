
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
* First get the collection id from Archive-It
* Run the following command
  
  ```detect_off_topic [collection_id]```
  
  For example:
   
  ```detect_off_topic 1234``` 
  
* Check a list of your off-topic mementos on the following directory after replacing 1234 with your collection_id
   
  ```cat data/collection_1234/off_topic_cosine_file.txt```