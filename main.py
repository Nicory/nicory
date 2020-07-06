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
import nest_asyncio # фикс asyncio для запуска нескольких хуевин
nest_asyncio.apply() # фикс asyncio для запуска нескольких хуевин

from Backend import RinokuBackend

from colorama import Fore, Style  # Цветная консоль
from colorama import init  # Цветная консоль
from discord.ext import commands


class NoPermission(commands.errors.CommandError):
    pass


class CommandDisabled(commands.errors.CommandError):
    pass


client = commands.AutoShardedBot(command_prefix="#")
client.remove_command("help")

status = config.status
init()

color = config.error_color

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

loop = Loop(client)
try:
    loop.activator()
except AssertionError:
    pass

client.add_cog(RinokuBackend(client))


@client.event
async def on_message(message):
    if not message.author.bot:
        if message.guild:
            mute_role = discord.utils.get(message.guild.roles, name="RB_Muted")
            if mute_role in message.author.roles:
                if mute_role not in message.author.roles:
                    pass
                else:
                    await message.delete()
            else:
                await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Команда не найдена!', color=color))
    elif isinstance(error, commands.MissingPermissions):
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, У бота недостаточно прав!\n'
                                                              f'Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций.', color=color))
    elif isinstance(error, commands.MissingPermissions) or isinstance(error, NoPermission):
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, У вас недостаточно прав!', color=color))
    elif isinstance(error, commands.BadArgument):
        if "Member" in str(error):
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Пользователь не найден!', color=color))
        if "Guild" in str(error):
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Сервер не найден!', color=color))
        else:
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Введён неверный аргумент!', color=color))
    elif isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Пропущен аргумент с названием {error.param.name}!', color=color))
    elif isinstance(error, CommandDisabled):
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, эта команда отключена!', color=color))
    else:
        if "ValueError: invalid literal for int()" in str(error):
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Укажите число а не строку!', color=color))
        else:
            print(Fore.RED + f"[ERROR] " + Style.RESET_ALL + f"Команда: {ctx.message.content}")
            print(Fore.RED + f"[ERROR] " + Style.RESET_ALL + f"Сервер:  {ctx.message.guild}")
            print(Fore.RED + f"[ERROR] " + Style.RESET_ALL + f"Ошибка:  {error}")
            await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, \n**`ERROR:`** {error}', color=color))
            raise error


# LUR Система
@client.command(hidden=True)
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'Modules.{extension}')

    print(Fore.YELLOW + "[RB Log] " + Style.RESET_ALL + f"Загружен модуль - {extension}")
    await ctx.send(f"Модуль **{extension}** успешно загружен!")


@client.command(hidden=True)
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'Modules.{extension}')

    print(Fore.YELLOW + "[RB Log] " + Style.RESET_ALL + f"Выгружен модуль - {extension}")
    await ctx.send(f"Модуль **{extension}** успешно выгружен!")


@client.command(hidden=True)
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    client.reload_extension(f'Modules.{extension}')
    print(Fore.YELLOW + "[RB Log] " + Style.RESET_ALL + f"Перезагружен модуль - {extension}")
    await ctx.send(f"Модуль **{extension}** успешно перезагружен!")


for file in os.listdir("./Modules"):
    if file.endswith(".py"):
        client.load_extension(f'Modules.{file[:-3]}')
        print(Fore.YELLOW + "[RB Log] " + Style.RESET_ALL + f"Module loaded - {file[:-3]}")


@client.check
async def permission_check(ctx):
    conn = pymongo.MongoClient(config.MONGODB)
    db = conn[f"RB_DB"]  # Подключаемся к нужно БД
    # Подключаемся к нужной колекции в нужной бд
    cursor = db[f"commands_permissions"]

    if cursor.find_one({"guild": ctx.guild.id, f'cmd_{ctx.command.name}': False}):
        raise CommandDisabled()
    else:
        return True

client.run(config.TOKEN)
