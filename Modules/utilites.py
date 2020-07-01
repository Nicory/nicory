# Импорт
# <!-- Дискорд -->
import discord
import pymongo
import config
from discord.ext import commands
from Cybernator import Paginator


# Код
class utilites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cog_name = ["Утилиты"]

    @commands.command(
        aliases=["хелп", "команды", "comms", "commands", "помощь"],
        description="Это сообщение")
    async def help(self, ctx):
        comm_num = 1
        embedlist = []

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"guild_settings_prefixes"]  # Подключаемся к нужной колекции в нужной бд
        prefix = cursor.find_one({"guild": f"{ctx.guild.id}"})["prefix"]

        for i in self.bot.cogs:
            cog = self.bot.cogs[i]
            name = cog.cog_name[0]
            hide = len(cog.cog_name)
            cogs_num = len(self.bot.cogs) - 1
            comm_list = []

            if hide == 1:
                for command in self.bot.commands:
                    if command.cog_name == i:
                        if not command.hidden:
                            comm_list.append(
                                f"`{prefix}{command.aliases[0]}` — {command.description}\n")

                embed = discord.Embed(
                    title=f"ПОМОЩЬ | {name} | {comm_num}/{cogs_num}",
                    description=f"".join(comm_list),
                    color=config.color)
                embed.set_footer(text="Rinoku Bot | Все права были зашифрованны в двоичный код", icon_url=self.bot.user.avatar_url)  # Сюда Текст и Иконку футера
                embed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/695787093242282055/707320024473534485/what.png')

                embedlist.append(embed)
                comm_num += 1

        message = await ctx.send(embed=embedlist[0])
        page = Paginator(self.bot, message, timeout=200, only=ctx.author, delete_message=True, time_stamp=True,
                         use_more=False,
                         embeds=embedlist, color=config.color, language="ru", footer=True, footer_icon=self.bot.user.avatar_url)  # Сюда Цвет и Текст футера
        await page.start()

    @commands.command(
        alises=["настройка-варны", "Настройка-варны"],
        description="Настроить максимальное количество предупрждений для бана")
    @commands.has_permissions(administrator=True)
    async def c_warns(self, ctx, arg):

        # Конект БД
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"guild_settings_max_warns"]  # Подключаемся к нужной колекции в нужной бд

        await ctx.send("Укажите максимальное количество варнов на сервере (у вас 3 минуты)")

        def check(m):
            return m.channel == ctx.channel

        try:
            arg = await self.bot.wait_for("message", check=check, timeout=180)
        except TimeoutError:
            return await ctx.send("Время закончилось.")

        db_arg = arg.content

        if cursor.find_one({"guild": f"{ctx.guild.id}"}):
            cursor.update_one({"guild": f"{ctx.guild.id}"}, {'$set': {"max_warns": db_arg}})

        else:
            cursor.insert_one({"guild": f"{ctx.guild.id}", "max_warns": db_arg})

        await ctx.send(f"Настройка успешна!")

    @commands.command(
        alises=["отключить"],
        description="Отключить команду")
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx, name: str):
        if name == "enable" or name == "disable":
            return await ctx.send("Эти команды нельзя отключить!")

        exists = False

        for command in self.bot.commands:
            if command.name == name:
                exists = True

        if exists == False:
            return await ctx.send("Такой команды не существует!")

        # Конект БД
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        # Подключаемся к нужной колекции в нужной бд
        cursor = db[f"commands_permissions"]

        if cursor.find_one({"guild": ctx.guild.id}):
            cursor.update_one({"guild": ctx.guild.id}, {"$set": {f'cmd_{name}': False}})

        else:
            cursor.insert_one({"guild": ctx.guild.id}, {
                              "$set": {ctx.command.name: False}})

        await ctx.send(f"Команда `{name}` успешно отключена!")

    @commands.command(
        alises=["включить"],
        description="Включить команду")
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx, name: str):

        if name == "enable" or name == "disable":
            return

        exists = False

        for command in self.bot.commands:
            if command.name == name:
                exists = True

        if exists == False:
            return await ctx.send("Такой команды не существует!")
  
        # Конект БД
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        # Подключаемся к нужной колекции в нужной бд
        cursor = db[f"commands_permissions"]

        if cursor.find_one({"guild": ctx.guild.id}):
            cursor.update_one({"guild": ctx.guild.id}, {
                              "$set": {f'cmd_{name}': True}})

        else:
            cursor.insert_one({"guild": ctx.guild.id}, {
                              "$set": {ctx.command.name: True}})

        await ctx.send(f"Команда `{name}` успешно включена!")


def setup(client):
    client.add_cog(utilites(client))
