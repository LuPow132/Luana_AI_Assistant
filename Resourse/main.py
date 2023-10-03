# This program making by LuPow to give everyone acess to Cute personal AI assitant to help you with everything in your daily life or even streaming like Vtuber
# 2023 LuPow @ STBUU IRoBot - Tustong Tongnumpen

#import library
import json
import asyncio
import aiohttp
from sentence_transformers import SentenceTransformer, util
import torch

#import configuration
import configuration

colab_api_llm = f"{configuration.cloudflareurl}/v1/generate"
name = configuration.name
context = configuration.prompt_personality
model = SentenceTransformer(configuration.llm_model)
relate_prompt_amount = configuration.relate_prompt_amount
file_location = configuration.conversation_log_location

#defind variable
conversationDB = []

#class llm to manage everything about llm
class LLM:
    async def api(message):
        params = {
            'max_new_tokens': 220,
            'temperature': 0.7,
            'top_p': 0.1,
            'repetition_penalty': 1.2,
            'top_k': 40,
            'seed': -1,
        }

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "prompt": message,
            "temperature": params["temperature"],
            "top_p": params["top_p"],
            "rep_pen": params["repetition_penalty"],
            'max_length': params["max_new_tokens"],
            "top_k": params["top_k"]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(colab_api_llm, headers=headers, json=data) as response:
                response_json = await response.json()

        generated_text = response_json["results"][0]["text"]

        response_text = generated_text.split('\n')[0]
        response_text = response_text.strip()
        
        return response_text
    
    def chat(message):
        prompt = conversation_Manger.prompt_maker(message)
        result = asyncio.run(LLM.api(prompt))
        print(result)
        conversation_Manger.appendConversation_to_Json("User",message,file_location)
        conversation_Manger.appendConversation_to_Json(name,result,file_location)


    
#class prompt that will manage everything about prompt and finding relate prompt
class conversation_Manger:
    #Load conversation from JsonL to list then embedding
    def conversationLoad():
        global conversationDB, vectordb, top_k

        #make conversationDB to empty
        conversationDB = []

        #Load file from jsonl to list
        with open(file_location, 'r') as file:
            for line in file:
                data = json.loads(line)
                conversationDB.append(data['person'] + ":" + data['message'])

        #embedding list to tensor
        vectordb = model.encode(conversationDB, convert_to_tensor=True,show_progress_bar=True)
        top_k = min(relate_prompt_amount, len(vectordb))
        
        

    def appendConversation_to_vectordb(person, message):
        global conversationDB,vectordb
        # conversation_Manger.appendConversation_to_Json()

        #set new list variable to append
        vectordb_append_text = [f'{person}:{message}'] 

        #encode it to vector
        vectordb_append = model.encode(vectordb_append_text, convert_to_tensor=True,show_progress_bar=True)
        
        #merge 2 vector and 2 list into one vector and one list
        conversationDB += vectordb_append_text
        vectordb = torch.cat((vectordb,vectordb_append),dim=0)

    #{"person": "A", "message": A} file format
    def appendConversation_to_Json(person, message, file_location):
        text =  str(f'{"person": {person}, "message": {message}}')
        print(text)
        try:
            # Open the file in append mode and create it if it doesn't exist
            with open(file_location, "a") as jsonl_file:
                # Write the JSON object on a new line
                jsonl_file.write(text + '\n')
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    #Find relate prompt from Tensor
    def find_similarity_prompt(query):
        # Find the closest 2 sentences of the corpus for each query sentence based on cosine similarity
        query_embedding = model.encode(query, convert_to_tensor=True)

        # We use cosine-similarity and torch.topk to find the highest scores
        cos_scores = util.cos_sim(query_embedding, vectordb)[0]
        top_results = torch.topk(cos_scores, k=top_k)

        # print(f"query_embed\tcos\ttop_result\tvector_db\n\n{len(query_embedding)}\t\t{len(cos_scores)}\t{len(top_results)}\t\t{len(vectordb)}\n\n")

        #return info
        result = ""
        for score, idx in zip(top_results[0], top_results[1]):
            print(idx)
            result += f'{conversationDB[idx]}\n'
        return result

        
    def prompt_maker(keyword):
        relate_prompt = conversation_Manger.find_similarity_prompt(keyword)

        text = f"{context} \n\n{relate_prompt} \nUser:{keyword} \n{name}:"
        return text
    
conversation_Manger.conversationLoad()
while True:
    message = input("User: ")
    LLM.chat(message)
#to calling LLM use
# asyncio.run(LLM_api(prompt))
