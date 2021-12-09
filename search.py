import retriever as ret
import corpus_loader as loader
import reader as r
from haystack.nodes import TransformersQueryClassifier


def print_helper(query, results, mode, round_of_search):
    to_return = ""

    if (len(results) == 0):
        to_return = "No Content Retrieved for Query No " + str(round_of_search) + " : " + query +  "\n\n"
    
    else:
        indx = 0
        for item in results:

            if mode == "succinct":
                
                context = item.context
                offsets_in_context = item.offsets_in_context[0]
                # print(offsets_in_context)
                start = offsets_in_context.start
                end   = offsets_in_context.end
                start_2   = None
                end_2     = None
                offsets_2 = None

                try:
                    offsets_2 = item.offsets_in_context[1]
                    start_2   = offsets_2.start
                    end_2     = offsets_2.end
                except IndexError:
                    pass

                # offsets_in_document = str(item.offsets_in_document[0])

                if to_return == "":
                    to_return = "Succinct Content Retrieved for Query No " + str(round_of_search) + " : " + query +  "\n\n"
                if start_2 != None and end_2 != None: 
                    to_return +=       "    " +         "Document " +               str(indx) + ": " + "\n" \
                                +  "        " +       "Summary 1: " +      context[start:end] + "\n" \
                                +  "        " +       "Summary 2: " + context[start_2: end_2] + "\n" \
                                +  "        " +    "Full context: " +                 context + "\n" 
                else:
                    to_return +=       "    " +         "Document " +               str(indx) + ": " + "\n" \
                                +  "        " +       "Summary 1: " +      context[start:end] + "\n" \
                                +  "        " +    "Full context: " +                 context + "\n" 
                    
            
            elif mode == "detailed":

                meta_data = item.meta
                institution = meta_data["institution"]
                name = meta_data["name"]

                type_var = item.content_type
                score = item.score
                context = item.content
                document_id = item.id


                if to_return == "":
                    to_return = "Detailed Content Retrieved for Query No " + str(round_of_search) + " : " +  query + "\n\n"
                
                to_return +=    "    " +     "Document " +   str(indx) + ": " + "\n" \
                          + "        " +        "Type: " +        type_var + "\n"  \
                          + "        " +       "Score: " +  str(score) + "\n" \
                          + "        " +      "Doc_ID: " + document_id + "\n" \
                          + "        " +        "Name: " +        name + "\n" \
                          + "        " + "Institution: " + institution + "\n" \
                          + "        " +"Full Context: " +     context + "\n" \
                            # + "        " + offsets_in_context + " in document\n" \
                            # + "        " + offsets_in_document + " in file\n\n"

            indx += 1

    to_return = "======================================================================================================\n======================================================================================================\n\n" \
                + to_return + \
                "======================================================================================================\n======================================================================================================\n\n"
    return to_return


def parse_filter(raw_filter):
    # raw_filter.replace(',', '')
    raw_filter.replace('\n', '')
    filter_list = raw_filter.split(" ", 1)
    
    filter_type = "name"
    if filter_list[0] == "--name":
        filter_type = "name"
    elif filter_list[0] == "--institution":
        filter_type = "institution"
    
    filter_content = filter_list[1].split("&")
    
    return filter_type, filter_content


def valid_filter(raw_filter):
    filter_list = raw_filter.split()

    if len(filter_list) <= 1:
        return False
    
    if filter_list[0] != "--name" and filter_list[0] != "--institution":
        return False
    if ',' in filter_list or  '.' in filter_list or '!' in filter_list or '@' in filter_list:
        return False


    return True


def run_searchEngine(filename):
    print("Loading corpus...")
    document_store = loader.create_documentStore(filename)
    elastic_retriever = ret.Retriever(document_store, "ElasticSearch")
    dense_retriever = ret.Retriever(document_store, "DensePassage")
    document_store.update_embeddings(dense_retriever.retriever)
    question_classifier = TransformersQueryClassifier(model_name_or_path="shahrukhx01/bert-mini-finetune-question-detection")
    reader = r.Reader()

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
            
            # query classification
            classification = question_classifier.run(query=raw_query)
            if classification[1] == "output_1":
                retriever = dense_retriever
            else:
                retriever = elastic_retriever

            # taking filters
            retriever.clear_filter()
            while True:
                raw_filter = input("Add filter on faculty name and use & to seperate multiple filters as '--name <NAME1>&<NAME2>& ...'" +  "\n" \
                                    +"Add filter on  institution and use & to seperate '--institution <INSTUTITION1>&<INSTITUTION2>&...'" + "\n" \
                                    +"Enter 'done' to finish" + "\n"\
                                    +"Enter 'clear' to clear filter"+"\n")
                if raw_filter == "done":
                    break
                if raw_filter == "clear":
                    retriever.clear_filter()
                    print("All filters are erased.")
                    continue
                if not valid_filter(raw_filter):
                    print("Invalid Filter!")
                    continue

                filter_type, filter_content = parse_filter(raw_filter)
                retriever.add_filter(filter_type, filter_content)
                print("Current filters: ", retriever.filters)
            

            try:
                candidate_documents = retriever.retrive(5, raw_query)     
                results = reader.predict(raw_query, candidate_documents)           
            except ValueError:
                f.write("\n\nNo Content Retrieved for Query No " + str(indx) + ": " + raw_query + "\n\n\n")
                print("\n\nNo Content Retrieved for Query No " + str(indx) + ": " + raw_query + "\n\n\n")
                continue
            
            # print(candidate_documents)
            # print(results["answers"])
            to_print = None
            # print(candidate_documents)
            if  (Mode == "succinct"):
                to_print = print_helper(raw_query, results["answers"], Mode, indx)
            elif(Mode == "detailed"):
                to_print = print_helper(raw_query, candidate_documents, Mode, indx)

            f.write(to_print)
            print(to_print)

            f.write("\n\n")
            


if __name__ == '__main__':
    run_searchEngine("test_corpus.txt")
