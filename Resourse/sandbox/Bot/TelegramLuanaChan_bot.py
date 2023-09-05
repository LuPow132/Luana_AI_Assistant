import json
import asyncio
import aiohttp
host = "https://xp-occasionally-coleman-specific.trycloudflare.com/api"
url = f"{host}/v1/generate"

async def api(context, prompt):
    modified_prompt = f"{context}\n\nUser: {prompt}\nLuana:"

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
        "top_k": params["top_k"], 
        'max_new_tokens': 250
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response_json = await response.json()

    generated_text = response_json["results"][0]["text"]

    response_text = generated_text.split('\n')[0]
    response_text = response_text.strip()
    
    return print(response_text)

#For bot
context = "Luanachan is a japanese vitrual anime girl that make to help Irobot member with everything. Like Finding Robot Part price, remind them about up coming event or even open music and talk to them like human being. She made by Lupow who lonely so much that he make this happend"


while True:
    prompt = input("enter message: ")
    asyncio.run(api(context,prompt))


