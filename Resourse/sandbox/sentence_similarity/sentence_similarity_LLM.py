from sentence_transformers import SentenceTransformer, util
import torch
import json

model = SentenceTransformer('all-MiniLM-L6-v2')

# Corpus with example sentences
conversationDB = []


def conversationLoad():
    global conversationDB, vectordb, top_k
    # Replace 'your_file.jsonl' with the actual filename
    with open('source/conversation.jsonl', 'r') as file:
        for line in file:
            # Load each line as a JSON object and append it to the list
            data = json.loads(line)
            conversationDB.append(data['person'] + ":" + data['message'])
    vectordb = model.encode(conversationDB, convert_to_tensor=True)
    top_k = min(5, len(vectordb))

def find_similarity_prompt(query):
    # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
    query_embedding = model.encode(query, convert_to_tensor=True)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(query_embedding, vectordb)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:\n\n")

    for score, idx in zip(top_results[0], top_results[1]):
        print(conversationDB[idx], "(Score: {:.4f})".format(score))

#{"person": "A", "message": A} file format
def appendConversation(message, file_location):
    try:
        # Open the file in append mode and create it if it doesn't exist
        with open(file_location, "a") as jsonl_file:
            # Write the JSON object on a new line
            jsonl_file.write(json.dumps(message) + '\n')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
conversationLoad()

while True:
    # Query sentences:
    query = input("input keyword: ")
    find_similarity_prompt(query)
