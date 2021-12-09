# YouTube Link
https://youtu.be/wRiY4Wuft04

# Scraper Instructions
### Installation
(The scraper was developed with Python 3.5.6 but later version probably shouldn't cause any issues.)

Note that the first two files are included in the repo so download/installation of them may not be necessary
- Install chromedriver96 from [here](https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/)
- Download the stanford-ner zip file from [here](https://nlp.stanford.edu/software/CRF-NER.shtml#Download). Extract in the project directory.

- Run the following commands:
```
pip install bs4
pip install nltk
pip install selenium
```

### Features
The primary function of the webscraper as compared to a scraper like that in the MPs was to make it more robust and capable of getting information from more than one website, rather than just being tailored to one website format. Our scraper operates by being given a school's faculty directory, and then attempts to click on links that are recognized as names and subsequently scrape all the text that comes from those links. 

However to get a more robust scraper, we had to relax certain constraints which also led to a few problems:
- There is sometimes information that is scraped that is irrelevant.
- The urllib library seems to cause issues with what we assume is protection against too many queries (inconsistently get 500 and 406 error codes)
- Limitations with the name recognition portion of the scraper can lead to irrelevant links/pages being scraped.

### Usage
Usage of the scraper is simple and easy to modify. Ensure all packages and requirements (chromedriver and stanford-ner folder) are downloaded and installed. Simply run all cells containing functions (which should be ```find_names()```, ```get_links()```, ```tag_visible()```, ```text_from_html()```, ```scrape_text()```, ```scrape_from_url()```, ```export_data()```)

Fill in your own url/base_url and run the cells that call ```scrape_from_url()``` and ```export_data()``` or create a new cell with the following code:
```
url = "https://cs.uoregon.edu/people/faculty"   # put your own url here!
base_url = 'https://cs.uoregon.edu/'            # put your own url here!

# run the scraper
names, bio_urls, bios = scrape_from_url(url, base_url)

# export the scraper results to a text file
export_data(names, bio_urls, bios)
```
# Search Engine Instructions

### Install Haystack
For default installation, run
`pip3 install farm-haystack`

However, there seems to be some release issues that cause import path errors. If that's the case, install by running 
````
git clone https://github.com/deepset-ai/haystack.git
cd haystack
pip install --editable .
````


To start a DocumentStore instance, run docker
````
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.9.2
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.9.2
````


Once Docker is running, you can run the search engine by running
`python search.py`


### Basic Features{Succinct/Detailed mode, Filters, and Query Classifier}
1. There is a succinct mode and a detailed mode in our search engine. At beginning of the search process, the user is asked to select the mode they prefer:
````
Mode = input("Indicate search mode(succinct or detailed): ")
while (Mode != "succinct" and Mode != "detailed"):
    Mode = input("Plz insert correct modes (either succinct or detailed): ")
````
The search engine will not continue only if you've inputted str of "succinct" or "detailed" exactly.

The succinct mode will return content in outputs like 

````
======================================================================================================
======================================================================================================

Succinct Content Retrieved for Query No 0 : who is nancy

    Document 0: 
        summary 1: professor
        Full context: Nancy Amato is a professor in department of computer science

    Document 1: 
        summary 1: Nancy Wang is a professor
        Full context: Nancy Wang is a professor from the Cornell University in the department of agriculture

    Document 2: 
        summary 1: Kris is a computer science professor
        Full context: Kris is a computer science professor who graduated from UCB

======================================================================================================
======================================================================================================

````
and detailed search would return results like 
````
======================================================================================================
======================================================================================================

Detailed Content Retrieved for Query No 0 : who is nancy

    Document 0: 
        Type: text
        Score: 0.6458722488407372
        Doc_ID: 19d83955ef8c4a9baed6d4d876412f18
        Name: nancy amato
        Institution: uiuc
        Full Context: Nancy Amato is a professor in department of computer science

    Document 1: 
        Type: text
        Score: 0.642917600171231
        Doc_ID: b7d2ac895a75c9975d61626a6dd9a01c
        Name: nancy wang
        Institution: cornell university
        Full Context: Nancy Wang is a professor from the Cornell University in the department of agriculture

======================================================================================================
======================================================================================================
````

2. We have also come up with some filter features to catch the right documents more accurately. We've only added two type of filters right now(name and institution) to do the work and might add more filters later on.
The usage for the filter is as follows.
````
"Add filter on faculty name and use & to seperate multiple filters as '--name <NAME1>&<NAME2>& ...'" +  "\n" \
"Add filter on  institution and use & to seperate '--institution <INSTUTITION1>&<INSTITUTION2>&...'" + "\n" \
"Enter 'done' to finish" + "\n"\
"Enter 'clear' to clear filter"+"\n")
````
        
Example output with filter        
````
Detailed Content Retrieved for Query No 0 : who is nancy

    Document 0: 
        Type: text
        Score: 0.6458722488407372
        Doc_ID: 19d83955ef8c4a9baed6d4d876412f18
        Name: nancy amato
        Institution: uiuc
        Full Context: Nancy Amato is a professor in department of computer science

    Document 1: 
        Type: text
        Score: 0.642917600171231
        Doc_ID: b7d2ac895a75c9975d61626a6dd9a01c
        Name: nancy wang
        Institution: cornell university
        Full Context: Nancy Wang is a professor from the Cornell University in the department of agriculture

````


Example output with filter{'name': ['nancy amato']}:

````
Detailed Content Retrieved for Query No 2 : who is nancy

    Document 0: 
        Type: text
        Score: 0.6458722488407372
        Doc_ID: 19d83955ef8c4a9baed6d4d876412f18
        Name: nancy amato
        Institution: uiuc
        Full Context: Nancy Amato is a professor in department of computer science

````

3. Thx to haystack lib in py, We have also implemented a Query Classifier. Since this is automatically built in, say if you inserted in "Who is nancy", it will be automatically assigned a tag of "Questions". Otherwise if you inserted in "nancy", it will be automatically assigned "keywords". We are using different retrievers for different types of query to achieve the optimal search performance.

````
from haystack.nodes import TransformersQueryClassifier
...
classification = question_classifier.run(query=raw_query)
    if classification[1] == "output_1":
        retriever = dense_retriever
    else:
        retriever = elastic_retriever
...
````
