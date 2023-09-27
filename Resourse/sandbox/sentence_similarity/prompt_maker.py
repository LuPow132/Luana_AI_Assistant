from sentence_transformers import SentenceTransformer, util
import torch
import json

#defind LLM model for find relate prompt
model = SentenceTransformer('all-MiniLM-L6-v2')

#Defind conversationDB as List
conversationDB = []

#Config
relate_prompt_amount = 2
file_location = "source/conversation.jsonl"

class conversation_Manger:
    #Load conversation from JsonL to list then embedding
    def conversationLoad():
        global conversationDB, vectordb, top_k

        #Load file
        with open(file_location, 'r') as file:
            for line in file:
                # Load each line as a JSON object and append it to the list
                data = json.loads(line)
                conversationDB.append(data['person'] + ":" + data['message'])

        #embedding list to tensor
        vectordb = model.encode(conversationDB, convert_to_tensor=True,show_progress_bar=True)
        top_k = min(relate_prompt_amount, len(vectordb))

    def appendConversation_to_Vector(person,message):
        global vectordb, top_k
        text = f'{person}:{message}'

        #embedding list to tensor
        vectordb = model.encode(text, convert_to_tensor=True,show_progress_bar=True)
        top_k = min(relate_prompt_amount, len(vectordb))

    #Find relate prompt from Tensor
    def find_similarity_prompt(query):
        # Find the closest 2 sentences of the corpus for each query sentence based on cosine similarity
        query_embedding = model.encode(query, convert_to_tensor=True)

        # We use cosine-similarity and torch.topk to find the highest scores
        cos_scores = util.cos_sim(query_embedding, vectordb)[0]
        top_results = torch.topk(cos_scores, k=top_k)

        #return info
        result = ""
        for score, idx in zip(top_results[0], top_results[1]):
            result += f'{conversationDB[idx]}\n'
        return result

    #{"person": "A", "message": A} file format
    def appendConversation_to_Json(message, file_location):
        try:
            # Open the file in append mode and create it if it doesn't exist
            with open(file_location, "a") as jsonl_file:
                # Write the JSON object on a new line
                jsonl_file.write(json.dumps(message) + '\n')
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            
    def prompt_maker(keyword):
        

        relate_prompt = conversation_Manger.find_similarity_prompt(keyword)

        text = f"You name is Luanachan. She is a Vtuber that made by LuPow to help assit IRobot member like doing research, be their friend, open any song. Luana personality is Kind, Funny and cute.\nhere is the prompt about past conversation you can use if it relate \n\n{relate_prompt}"
        return text
    
#Load pass conversation at the start
conversation_Manger.conversationLoad()
  
while True: 
    # Query sentences:
    query = input("input keyword: ")
    print(conversation_Manger.prompt_maker(query))
