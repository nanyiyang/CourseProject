# importing necessary dependencies

from haystack.document_store import ElasticsearchDocumentStore


def load_text_corpus(filename):
    """
    This methods takes in a text file, reads its content and convert the content into a list of
    dictionaries for Haystack to build a DocumentStore
    """

    with open(filename, "r") as f:
        lines = f.readlines()

    corpus_list = []
    entry_dict = {}
    meta_dict = {}
    for i in range(len(lines)):
        line = lines[i]

        # even index ==> attribute line
        if i % 2 == 0:
            entry_dict = {}
            meta_dict = {}
            line = line.replace('\n', '')
            features = line.split(',')
            meta_dict["name"] = features[0]
            meta_dict["institution"] = features[1]

        # odd index ==> text body
        else:
            entry_dict["content"] = line
            entry_dict['meta'] = meta_dict
            corpus_list.append(entry_dict)

    return corpus_list


def create_documentStore(filename):
    """
    This methods takes in a text file and creates an ElasticsearchDocumentStore based on its content
    Note: you might be warning Object ElasticsearchDocumentStore... a deprecated path. This is because
    the dev team of Haystack refactored their code, but the new code structure is not yet reflected in
    the newest release. So we are currently using an old import path
    """
    corpus_list = load_text_corpus(filename)
    document_store = ElasticsearchDocumentStore()
    document_store.write_documents(corpus_list)
    return document_store


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_documentStore("test_corpus.txt")
