import json, csv
import numpy
import math

min_time = []   # A list containing one value, i.e., the earliest article
max_time = []   # A list containing one value, i.e., the latest article


def search_refine(query=str, body=list, title=list, time=list):
    alpha_1 = float(.2)
    alpha_2 = float(.5)
    alpha_3 = float(.3)
    query_vector = create_query_vector(query)   # A vector=hash-table of term frequencies of the query ->(word, tf)
    title_vectors = create_title_vectors(title) # A list of hash-tables, where every hash-table is a corresponding vector of term frequencies of the title
    documents_hash_tables = create_doc_hash_tables(body)    # A list of hash-tables, where every hash-table is a collapsed document as key(word)->value(tf)
    discretized_time = create_time_values(time) # A hash-table of days from earliest to latest article. Convert dates into days, and create discretized time
    doc_frequencies = compute_doc_frequencies(documents_hash_tables, query_vector)  # A list of inverse doc frequencies, for every document
    scores = []
    for i in range(len(body)):
        score_title = dot_product(query_vector, title_vectors[i])
        score_body = okapi_product(query_vector, documents_hash_tables[i], doc_frequencies, len(body))
        time_score = score_time(discretized_time[i])
        score_final = float(alpha_1*(time_score/(max_time[0] - min_time[0]))) + alpha_2*float(score_body) + float(alpha_3*score_title)
        scores.append((score_final, i))
    # scores.sort(reverse=True)	# 1 # Edit to make sure that, it is not sorted based on the second element in the tuple
    # Use the i-d of the element in the tuple of scores[] to pull out the corresponding article and re-rank accordingly
    # 2 # Convert the list to json, and return the json, so that the appropriate articles may be shown on the web-search
    return scores


def create_query_vector(query=str):
    query_words = query.split(" ")
    query_hash = {}
    for i in range(len(query_words)):
        if query_words[i] in query_hash:
            query_hash[query_words[i]][1] += 1
        else:
            query_hash[query_words[i]] = [query_words[i], 1]
    return query_hash


def create_title_vectors(title=list):
    title_hash = []
    for i in range(len(title)):
        temp_hash = {}
        title_words = (title[i]).split(" ")
        for j in range(len(title_words)):
            if title_words[j] in temp_hash:
                temp_hash[title_words[j]][1] += 1
            else:
                temp_hash[title_words[j]] = [title_words[j], 1]
        title_hash.append(temp_hash)
        temp_hash.clear()
    return title_hash


def create_doc_hash_tables(body=list):
    body_hash = []
    for i in range(len(body)):
        temp_hash = {}
        body_words = (body[i]).split(" ")   # 3 # We need to check for regular expressions here. Replace split, and get rid of stop words.
        for j in range(len(body_words)):
            if body_words[j] in temp_hash:
                temp_hash[body_words[j]][1] += 1
            else:
                temp_hash[body_words[j]] = [body_words[j], 1]
        body_hash.append(temp_hash)
        temp_hash.clear()
    return body_hash


def create_time_values(time=list):
    # Assuming time[] strings are of format -> mm/dd/yyyy
    curr_min = 1000000
    curr_max = 0    # Just an initialization. We need to first convert the dates into days. Custom hash = year*365 + month*30 + day*1
    time_discrete = []
    for i in range(len(time)):
        curr_time = (time[i]).split("/")
        disc_value = int(curr_time[0])*30 + int(curr_time[1]) + int(curr_time[2])*365
        if disc_value < curr_min:
            curr_min = disc_value
        if disc_value > curr_max:
            curr_max = disc_value
        time_discrete.append(disc_value)
    max_time.append(curr_max)
    min_time.append(curr_min)
    return time_discrete


def compute_doc_frequencies(documents_hash_tables, query_vector):
    doc_frequencies = {}
    for key in query_vector:
        sum_docs = 0
        for j in range(len(documents_hash_tables)):
            if key in documents_hash_tables[j]:
                sum_docs += 1
        doc_frequencies[key] = sum_docs
    return doc_frequencies


def dot_product(query_vector, title_vector):
    dot_p = float(0)
    if len(query_vector) > len(title_vector):
        for key in query_vector:
            if key in title_vector:
                dot_p += title_vector[key][1]*query_vector[key][1]
    else:
        for key in title_vector:
            if key in query_vector:
                dot_p += title_vector[key][1]*query_vector[key][1]
    return dot_p


def score_time(discretized_time):
    return discretized_time - min_time[0]


def okapi_product(query_vector, document_hash_table, document_frequency, num_docs):
    score_of = float(0)
    for key in query_vector:
        if key in document_hash_table:
            score_of += okapi_score(query_vector[key][1], document_hash_table[key][1], document_frequency[key], num_docs)
    return score_of


def okapi_score(query_tf, doc_tf, idf, num_docs):
    k3 = float(.3)
    k1 = float(.1)
    score_o = idf_score(idf, num_docs)*float(doc_tf*(k1 + 1)/(doc_tf + k1))*float(query_tf*(k3 + 1)/(query_tf + k3))
    return score_o		# 4 # Add a little loop to remember the greatest document length and insert doc length norm


def idf_score(idf_freq, num_docs):
    return float(math.log((num_docs - idf_freq + float(.5))/(idf_freq + float(.5))))








