import os
import random
import re
import json

import requests as rq
import discord
from dotenv import load_dotenv

from curr import get_currency

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_guild_join(guild):
    await guild.text_channels[0].send("I love this place! I convert currency between USD and RMB, use `!help` to see commands")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if len(message.content) > 0 and isinstance(message.content, str):
        message.content = message.content.lower()

    # for help page, temp
    if message.content.strip() == "!help":
        help_str = """
        ```
Commands are NOT case-sensitive:
  We have default setting to translate currency between rmb and usd as below:
    !usd {num}: converts usd to rmb
    !rmb {num}: converts rmb to usd
  
  However, it now supports translation between any specified currencies:
    !rmb-nzd {num}
    !nzd-usd {num}```
        """
        await message.channel.send(help_str)

    # goodnight command
    if message.content.strip() == "!goodnight":
        help_str = """Goodnight Sir, good job for the day!
        """
        await message.channel.send(help_str)

    ####### General Approach #######
    command = message.content[:8]
    if command.count("-") == 1:
        num = message.content[8:].strip()
        num = float(num)
        command_split = command.split("-")
        from_curr = command_split[0].upper()[1:]
        to_curr = command_split[1].upper()
        key = from_curr + to_curr + "=X"
        curr = get_currency(key)
        await message.channel.send("fetching currency...")
        await message.channel.send(f"{from_curr} {round(num, 4)} is equivalent to {round(curr * num, 4)} in {to_curr}")

    ####### General Approach #######
    # if general approach failed 
    # good chance we just want the default translation between rmb and usd

    ####### Default Approach #######
    else:
        command = message.content[:4]
        if command == "!usd" or command == "!rmb":
            await message.channel.send("fetching currency...")
            message_split = message.content.split(" ")

            # if we do follow '!usd xxx(in rmb format)'
            if len(message_split) >= 2:
                num_str = message_split[1]
                try:
                    num = float(num_str)

                except:
                    print(f"don't recognize amount {num}")

                if command == "!rmb":
                    curr = get_currency("CNYUSD=X")
                    convert_curr_str = "usd"

                elif command == "!usd":
                    curr = get_currency("USDCNY=X")
                    convert_curr_str = "rmb"

                command_to_print = command[1:]
                command_to_print = command_to_print.upper()
                convert_curr_str = convert_curr_str.upper()
                await message.channel.send(f"{command_to_print} {round(num, 4)} is equivalent to {round(curr * num, 4)} in {convert_curr_str}")
    ####### Default Approach #######

client.run(TOKEN)


