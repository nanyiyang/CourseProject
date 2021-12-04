from haystack.nodes import FARMReader

class Reader:

    def __init__(self):
        model = "deepset/roberta-base-squad2"
        self.reader = FARMReader(model, use_gpu=True)

    def predict(self, query, documents, top_k=1):
        result = self.reader.predict(query=query, documents=documents, top_k=top_k)
        return result
