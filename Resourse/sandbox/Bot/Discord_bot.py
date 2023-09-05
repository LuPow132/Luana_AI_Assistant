from nextcord.ext import commands
import nextcord
import TelegramLuanaChan_bot
import time

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="",intents=intents)

# @bot.command(name="hi",intents=intents)
# async def SendMessage(ctx.message.text):
#     await ctx.send('Hello!')

@bot.command(name="ttm",intents=intents)
async def ttm(ctx):
    print(f'Recieve:{ctx.message.content}')
    responsed = await(TelegramLuanaChan_bot.get_responed((ctx.message.content).replace("ttm","")))
    print(f'Responsed:{responsed}')
    await ctx.send(responsed)

@bot.command(name="ut",intents=intents)
async def ut(ctx):
    uptime = round(time.time() - start_time)
    await ctx.send(f'{uptime} seconds')
    




@bot.event
async def on_ready():
    global start_time
    print(f'Login as {bot.user.name}')
    start_time = time.time()

if __name__ == '__main__':
    bot.run("MTE0NjY0NjY2NjQzOTU2MTMwNg.GgJqAA.SGk0ikeQYhRTHKwA7T3G6EWnDLPKQP0kcJx9kQ")