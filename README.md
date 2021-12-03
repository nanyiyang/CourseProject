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


Once Docker is running, you can run the search engine by entering
`python search.py`

