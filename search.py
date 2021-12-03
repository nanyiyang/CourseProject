import retriever as ret
import corpus_loader as loader


def run_searchEngine(filename):
    print("Loading corpus...")
    document_store = loader.create_documentStore(filename)
    retriever = ret.Retriever(document_store)

    print("Corpus loaded! Search engine running...")
    search_engine_running = True
    while search_engine_running:
        raw_query = input("Enter your raw search query as: ")
        if raw_query == "q":
            break

        candidate_documents = retriever.retrive(1, raw_query)
        print(candidate_documents)


if __name__ == '__main__':
    run_searchEngine("test_corpus.txt")
