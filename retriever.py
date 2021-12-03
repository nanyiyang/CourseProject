from haystack.nodes import ElasticsearchRetriever


class Retriever:
    """
    A retriever class to retrieve text based on queries with dynamic filters
    """

    def __init__(self, document_store):
        self.retriever = ElasticsearchRetriever(document_store)
        self.filters = {}

    def add_filter(self, filter_name, filter_vals):
        self.filters[filter_name] = filter_vals

    def clear_filter(self):
        self.filters = {}

    def retrive(self, top_k, query):
        candidate_documents = self.retriever.retrieve(query=query, top_k=top_k, filters=self.filters)
        return candidate_documents
