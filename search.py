import retriever as ret
import corpus_loader as loader
import reader as r

def print_helper(query, results, mode, round_of_search):
    to_return = ""

    if (len(results) == 0):
        to_return = "No Content Retrieved for Query No " + str(round_of_search) + " : " + query +  "\n\n"
    
    else:
        indx = 0
        for item in results:

            meta_data = item.meta
            institution = meta_data["institution"]
            name = meta_data["name"]

            type = item.content_type
            score = item.score
            context = item.content
            # offsets_in_document = str(item.offsets_in_document[0])
            # offsets_in_context = str(item.offsets_in_context[0])
            document_id = item.id
            
            if   mode == "succinct":
                if to_return == "":
                    to_return = "Succinct Content Retrieved for Query No " + str(round_of_search) + " : " + query +  "\n\n"
                to_return += "    " + "Document " + str(indx) + ": " + "\n" \
                    + "        " + context + "\n"
            
            elif mode == "detailed":
                if to_return == "":
                    to_return = "Detailed Content Retrieved for Query No " + str(round_of_search) + " : " +  query + "\n\n"
                
                to_return += "    " + "Document " + str(indx) + ": " + "\n" \
                    + "        " + "type: " + type + "\n"  \
                    + "        " + "score: " + str(score) + "\n" \
                    + "        " + "doc_ID: " + document_id + "\n" \
                    + "        " + "Name: " + name + "\n" \
                    + "        " + "Institution: " + institution + "\n" \
                    + "        " + "context: " + context + "\n" \
                    # + "        " + offsets_in_context + " in document\n" \
                    # + "        " + offsets_in_document + " in file\n\n"

            indx += 1

    to_return = "======================================================================================================\n======================================================================================================\n\n" \
                + to_return + \
                "======================================================================================================\n======================================================================================================\n\n"
                
    return to_return

def run_searchEngine(filename):
    print("Loading corpus...")
    document_store = loader.create_documentStore(filename)
    retriever = ret.Retriever(document_store)
    # reader = r.Reader()

    print("Corpus loaded! Search engine running...Plz select your mode\n")
    
    Mode = input("Indicate search mode(succinct or detailed): ")
    while (Mode != "succinct" and Mode != "detailed"):
        Mode = input("Plz insert correct modes (either succinct or detailed): ")
    

    search_engine_running = True
    indx = -1
    with open("output.txt", "a") as f:
        while search_engine_running:
            indx += 1
            raw_query = input("Enter your raw search query as: ")
            # quiting executions
            if raw_query == "quit":
                f.close()
                break

            try:
                candidate_documents = retriever.retrive(10, raw_query)     
                # results = reader.predict(raw_query, candidate_documents)           
            except ValueError:
                f.write("\n\nNo Content Retrieved for Query No " + str(indx) + ": " + raw_query + "\n\n\n")
                print("\n\nNo Content Retrieved for Query No " + str(indx) + ": " + raw_query + "\n\n\n")
                continue
            
            # print(candidate_documents)

            to_print = print_helper(raw_query, candidate_documents, Mode, indx)
            f.write(to_print)
            print(to_print)

            f.write("\n\n")
            


if __name__ == '__main__':
    run_searchEngine("test_corpus.txt")
