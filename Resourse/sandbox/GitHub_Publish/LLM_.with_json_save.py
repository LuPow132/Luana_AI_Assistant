#Import all library
import json
import asyncio
import aiohttp
import configuration
from rake_nltk import Rake

#Variable setting from configuration.py
url = f"{configuration.cloudflareurl}/v1/generate"
prompt_personality = configuration.prompt

#defind class
class prompt_manager:
    def prompt_maker(message):
        related_prompt = prompt_manager.find_related_prompt(message)
        prompt = f'{prompt_personality}]n This is the past coversation you can use if it relate. {related_prompt}'

    def find_related_prompt(message):
        rake.extract_keywords_from_text(message)
        return rake.get_ranked_phrases()[:3]

class server_manager:
    #For bot
    async def api(context, prompt):
        modified_prompt = f"{context}\n\nUser: {prompt}\n{configuration.name}"
        

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
            "prompt": modified_prompt,
            "temperature": params["temperature"],
            "top_p": params["top_p"],
            "rep_pen": params["repetition_penalty"],
            'max_length': params["max_new_tokens"],
            "top_k": params["top_k"]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                response_json = await response.json()

        generated_text = response_json["results"][0]["text"]

        response_text = generated_text.split('\n')[0]
        response_text = response_text.strip()
        
        return response_text

class client:
    def runtime():
        prompt = input("Enter message: ")
        asyncio.run(api(context,prompt))


rake = Rake()

while True:
    client.runtime()
