# _____  _             _          ____        _
# |  __ \(_)           | |        |  _ \      | |
# | |__) |_ _ __   ___ | | ___   _| |_) | ___ | |_
# |  _  /| | '_ \ / _ \| |/ / | | |  _ < / _ \| __|
# | | \ \| | | | | (_) |   <| |_| | |_) | (_) | |_
# |_|  \_\_|_| |_|\___/|_|\_\\__,_|____/ \___/ \__|

# Импорт библиотек
import asyncio
import time
from loops import Loop

import discord
import config
import os
import pymongo

from colorama import Fore, Back, Style  # Цветная консоль
from colorama import init  # Цветная консоль
from discord.ext import commands

status = config.status
Loop.activator()
init()

client = commands.Bot(command_prefix="#")
client.remove_command("help")


@client.event
async def on_ready():
    print(" ")
    print(" _____  _             _          ____        _   ")
    print("|  __ \(_)           | |        |  _ \      | |  ")
    print("| |__) |_ _ __   ___ | | ___   _| |_) | ___ | |_ ")
    print("|  _  /| | '_ \ / _ \| |/ / | | |  _ < / _ \| __|")
    print("| | \ \| | | | | (_) |   <| |_| | |_) | (_) | |_ ")
    print("|_|  \_\_|_| |_|\___/|_|\_/\__,_|____/ \___/ \__|")
    print(" ")
    print(Fore.CYAN + "===================================" + Style.RESET_ALL)
    print(f'  Запущена инициализация системы...          ')
    print(f'  Status   - {status}          ')
    await client.change_presence(activity=discord.Game(name=status))
    print(f'  Bot Name - {client.user.name}')
    print(f'  Bot Id   - {client.user.id}  ')
    print(Fore.CYAN + "===================================" + Style.RESET_ALL)
    print(" ")


for file in os.listdir("./Modules"):
    if file.endswith(".py"):
        client.load_extension(f'Modules.{file[:-3]}')
        print(Fore.YELLOW + "[RB Log] " + Style.RESET_ALL + f"Module loaded - {file[:-3]}")


@client.event
async def on_message(message):
    mute_role = discord.utils.get(message.guild.roles, name="RB_Muted")
    if mute_role in message.author.roles:
        await message.delete()
    else:
        await client.process_commands(message)


# LUR Система
@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'Modules.{extension}')

    print(Fore.YELLOW + "[RB Log] " + Style.RESET_ALL + f"Загружен модуль - {extension}")
    await ctx.send(f"Модуль **{extension}** успешно загружен!")


@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'Modules.{extension}')

    print(Fore.YELLOW + "[RB Log] " + Style.RESET_ALL + f"Выгружен модуль - {extension}")
    await ctx.send(f"Модуль **{extension}** успешно выгружен!")


@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    client.reload_extension(f'Modules.{extension}')
    print(Fore.YELLOW + "[RB Log] " + Style.RESET_ALL + f"Перезагружен модуль - {extension}")
    await ctx.send(f"Модуль **{extension}** успешно перезагружен!")

client.run(config.TOKEN)
