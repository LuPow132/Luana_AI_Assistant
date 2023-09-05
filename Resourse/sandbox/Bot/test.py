#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
import API_KEY

import json
import asyncio
import aiohttp
host = "https://nut-bibliography-tuition-it.trycloudflare.com/api"
url = f"{host}/v1/generate"

API_TOKEN = API_KEY.telegram_key
# context = "Luanachan is a japanese vitrual anime girl that make to help Irobot member with everything. Like Finding Robot Part price, remind them about up coming event or even open music and talk to them like human being. She made by Lupow who lonely so much that he make this happend"
context = "Luanachan is a japanese vitrual anime girlfriends that make to act like girlfreinds to help people from lonely. talk to them like human being. She made by Lupow who lonely so much that he make this happend"

bot = telebot.TeleBot(API_TOKEN)

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
        "top_k": params["top_k"]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response_json = await response.json()

    generated_text = response_json["results"][0]["text"]

    response_text = generated_text.split('\n')[0]
    response_text = response_text.strip()
    
    return response_text


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi I am Luanachan! I'm here to help you with anything. Feel free to ask me anything!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    print(f"recieve:{message.text}")
    Reply = asyncio.run(api(context,message.text))
    print(f'Reply:{Reply}')
    bot.reply_to(message, Reply)


bot.infinity_polling()