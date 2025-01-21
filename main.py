import os

os.system("pip install -r requirements.txt")
import asyncio
import traceback
from threading import Thread
from datetime import datetime

import aiohttp
import discord
from discord.ext import commands


from core import Context
from core.Cog import Cog
from core.Olympus import Olympus
from utils.Tools import *
from utils.config import *
from dotenv import load_dotenv
import jishaku
import cogs 



#Configuring Jishaku behavior
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "False"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"


client = Olympus()
tree = client.tree
load_dotenv()
TOKEN = os.getenv("TOKEN")




@client.event
async def on_ready():
    await client.wait_until_ready()
    
    print("""
           \033[1;35m

        ____   ___  _   _ _   _ 
       / ___| / _ \| \ | | | | |
       \___ \| | | |  \| | | | |
        ___) | |_| | |\  | |_| |
       |____/ \___/|_| \_| \___/ 

       \033[0m
           """)
    print("Loaded & Online!")
    print(f"Logged in as: {client.user}")
    print(f"Connected to: {len(client.guilds)} guilds")
    print(f"Connected to: {len(client.users)} users")
    try:
        synced = await client.tree.sync()
        all_commands = list(client.commands)
        print(f"Synced Total {len(all_commands)} Client Commands and {len(synced)} Slash Commands")
    except Exception as e:
        print(e)


@client.event
async def on_command_completion(context: commands.Context) -> None:
    if context.author.id == 1070619070468214824:
        return

    full_command_name = context.command.qualified_name
    split = full_command_name.split("\n")
    executed_command = str(split[0])
    webhook_url = "https://discord.com/api/webhooks/1252219587043528715/5x6f-jZoBajQ3mUVDnP2_ecd5yalg8ff_Stc2L9zxSuuVc51Hyihp4MKyIgXtThY91j7"
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, session=session)

        if context.guild is not None:
            try:
                embed = discord.Embed(color=0x000000)
                avatar_url = context.author.avatar.url if context.author.avatar else context.author.default_avatar.url
                embed.set_author(
                    name=f"Executed {executed_command} Command By : {context.author}",
                    icon_url=avatar_url
                )
                embed.set_thumbnail(url=avatar_url)
                embed.add_field(name="<:right:1244660443323306118> Command Name :",
                                value=f"{executed_command}",
                                inline=False)
                embed.add_field(
                    name="<:right:1244660443323306118> Command Executed By :",
                    value=f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                    inline=False)
                embed.add_field(
                    name="<:right:1244660443323306118> Command Executed In :",
                    value=f"{context.guild.name} | ID: [{context.guild.id}](https://discord.com/guilds/{context.guild.id})",
                    inline=False)
                embed.add_field(
                    name="<:right:1244660443323306118> Command Executed In Channel :",
                    value=f"{context.channel.name} | ID: [{context.channel.id}](https://discord.com/channels/{context.guild.id}/{context.channel.id})",
                    inline=False)

                embed.timestamp = discord.utils.utcnow()
                embed.set_footer(text="Olympus Development™ ❤️",
                                 icon_url=client.user.display_avatar.url)

                
                await webhook.send(embed=embed)
            except Exception as e:
                print(f'Command failed: {e}')
                traceback.print_exc()
        else:
            try:
                embed1 = discord.Embed(color=0x000000)
                avatar_url = context.author.avatar.url if context.author.avatar else context.author.default_avatar.url
                embed1.set_author(
                    name=f"Executed {executed_command} Command By : {context.author}",
                    icon_url=avatar_url
                )
                embed1.set_thumbnail(url=avatar_url)
                embed1.add_field(name="<:right:1244660443323306118> Command Name :",
                                 value=f"{executed_command}",
                                 inline=False)
                embed1.add_field(
                    name="<:right:1244660443323306118> Command Executed By :",
                    value=f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
                    inline=False)
                embed1.set_footer(text=f"Powered by Olympus Development™",
                                  icon_url=client.user.display_avatar.url)
                print("Sending embed1 to webhook...")
                await webhook.send(embed=embed1)
                print("Embed1 sent successfully.")
            except Exception as e:
                print(f'Command failed: {e}')
                traceback.print_exc()


from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route('/')
def home():
    return f"© Olympus Development 2024"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()


keep_alive()


async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await client.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded {filename}')
            except Exception as e:
                print(f'Failed to load {filename}')
                traceback.print_exc()


async def main():
    async with client:
        os.system("clear")
        await client.load_extension("cogs")
        await client.load_extension("jishaku")
        await client.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
