# This program making by LuPow to give everyone acess to Cute personal AI assitant to help you with everything in your daily life or even streaming like Vtuber
# 2023 LuPow @ STBUU IRoBot - Tustong Tongnumpen

#import library
import json
import asyncio
import aiohttp
from sentence_transformers import SentenceTransformer, util
import torch
import threading
import time

#import configuration
import configuration

colab_api_llm = f"{configuration.cloudflareurl}/v1/generate"
name = configuration.name
context = configuration.prompt_personality
model = SentenceTransformer(configuration.llm_model)
relate_prompt_amount = configuration.relate_prompt_amount
file_location = configuration.conversation_log_location
example_conversation = configuration.example_conversation
Username = configuration.Username
context_amount = configuration.context_load_amount

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
        global prompt,result
        prompt = conversation_Manger.prompt_maker(message)
        result = asyncio.run(LLM.api(prompt))
        print(result)
        
    def save_chat():
        threading.Thread(conversation_Manger.appendConversation_to_Json(Username,message,file_location))
        threading.Thread(conversation_Manger.appendConversation_to_Json(name,result,file_location))
        threading.Thread(conversation_Manger.appendConversation_to_vectordb(Username,message))
        threading.Thread(conversation_Manger.appendConversation_to_vectordb(name,result))


    
#class prompt that will manage everything about prompt and finding relate prompt
class conversation_Manger:
    #Load conversation from JsonL to list then embedding
    def conversationLoad():
        global conversationDB, vectordb, top_k

        #make conversationDB to empty
        conversationDB = []

        with open(file_location, 'r', encoding='utf-8') as file:
        # Read each line in the file and append it to the list
            for line in file:
                conversationDB.append(line.strip())

        #embedding list to tensor
        vectordb = model.encode(conversationDB, convert_to_tensor=True,show_progress_bar=True)
        top_k = min(relate_prompt_amount, len(vectordb))
        
        

    def appendConversation_to_vectordb(person, message):
        global conversationDB,vectordb
        # conversation_Manger.appendConversation_to_Json()

        #set new list variable to append
        vectordb_append_text = [f'{person}:{message}'] 

        #encode it to vector
        vectordb_append = model.encode(vectordb_append_text, convert_to_tensor=True)
        
        #merge 2 vector and 2 list into one vector and one list
        conversationDB += vectordb_append_text
        vectordb = torch.cat((vectordb,vectordb_append),dim=0)

    #{"person": "A", "message": A} file format
    def appendConversation_to_Json(person, message, file_location):
        text =  f'{person}:{message}'
        # Open the file in append mode ('a')
        with open(file_location, 'a', encoding='utf-8') as file:
            # Write the new line to the file, including a newline character '\n'
            file.write(text + '\n')

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
            result += f'{conversationDB[idx]}\n'
        return result

    def context_Load():
        # Open the file in read mode
        with open(file_location, 'r', encoding='utf-8') as file:
            # Read all lines from the file and append them to the list
            all_lines = file.readlines()

        context_amount_k = min(len(all_lines),context_amount)
        # Extract the last two lines from the list
        if len(all_lines) >= context_amount_k:
            last_lines = all_lines[-context_amount_k:]

        return last_lines
        
    def prompt_maker(keyword):
        relate_prompt = conversation_Manger.find_similarity_prompt(keyword)
        context_past = "".join(conversation_Manger.context_Load())

        # text = f"{context} \n\nThis is a relate prompt you can use if it relate:\n{relate_prompt} \nThis is an example of how should you responsed:\n{example_conversation}\n\nNow answer to this conversation.\n{context_past}{Username}:{keyword} \n{name}:"
        text = f"{context} \n\nThis is a relate prompt you can use if it relate:\n{relate_prompt} \nNow answer to this conversation.\n{example_conversation}\n{context_past}{Username}:{keyword} \n{name}:"
        # print("-")
        # print(text)
        # print("-")
        return text
    
conversation_Manger.conversationLoad()
while True:
    message = input("User: ")
    start_time = time.time()
    LLM.chat(message)
    print(f'{round(time.time()-start_time,3)}s')
    LLM.save_chat()
