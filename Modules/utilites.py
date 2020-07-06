# Импорт
# <!-- Дискорд -->
import discord
import pymongo
import config
from discord.ext import commands
from Cybernator import Paginator
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import io


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
            cursor.insert_one({"guild": ctx.guild.id, f'cmd_{name}': False})

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
            cursor.insert_one({"guild": ctx.guild.id, f'cmd_{name}': True})

        await ctx.send(f"Команда `{name}` успешно включена!")

    # userinfo
    @commands.command(
        aliases=["Юзеринфо", "юзеринфо", "юзер", "Юзер", "User", "user", "Userinfo"]
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def userinfo(self, ctx, Member: discord.Member = None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_economy"]  # Подключаемся к экономике
        cursor_moder = db[f"members_warns"]  # Подключаемся к варнам

        if not Member:
            Member = ctx.author

        check_warns = cursor_moder.find(
            {
                "guild": f"{ctx.guild.id}",
                "member": f"{Member.id}"
            }
        )

        warns = check_warns.count()

        if not warns:
            warns = 0

        bal = cursor.find_one(
            {
                "guild": f"{ctx.guild.id}",
                "m_id": f"{Member.id}"
            }
        )
        if not bal:
            bal = "0"
        else:
            bal = bal['money']

        img = Image.new("RGBA", (920, 230), (0, 0, 0, 0))
        url = str(Member.avatar_url)[:-10]

        response = requests.get(url, stream=True)
        response = Image.open(io.BytesIO(response.content))
        response = response.convert('RGBA')
        response = response.resize((220, 220), Image.ANTIALIAS)
        img.paste(response, (5, 5, 225, 225))

        # создание изображения на основе картинки из файла PSD
        path = './Data/Template/'
        cache = './Data/Cache/'

        banner = Image.open(path+"background.png")
        banner = banner.convert('RGBA')
        img.paste(banner, (0, 0, 920, 230), banner)

        idraw = ImageDraw.Draw(img)
        name = Member.display_name
        tag = Member.discriminator

        headline = ImageFont.truetype(path + "arial.ttf", size=50)
        maintext = ImageFont.truetype(path + "andromeda.ttf", size=30)
        roletext = ImageFont.truetype(path + "andromeda.ttf", size=45)
        undertext = ImageFont.truetype(path + "andromeda.ttf", size=12)

        idraw.text((230, 37), f'{name}#{tag}', font=headline)
        idraw.text((328, 105), f'{Member.id}', font=maintext)
        idraw.text((685, 78), f"{bal} §", font=roletext)
        idraw.text((685, 115), f"{Member.status}", font=roletext)
        idraw.text((685, 165), f"{warns}", font=roletext)
        img.save(cache+'user_card.png')
        await ctx.message.delete()
        await ctx.send(file=discord.File(fp=cache+'user_card.png'))

    @commands.command(aliases=["Ping", "пинг", "Пинг"])
    async def ping(self, ctx):
        await ctx.send(f"{self.bot.ws.latency * 1000:.0f} мс")

    @commands.command(aliases=["Bot", "Бот", "бот"])
    async def bot(self, ctx):

        servers = len(self.bot.guilds)

        embed = discord.Embed(title="Я - мультисерверный Discord бот",
                              description="",
                              color=config.color)
        embed.set_author(name="Информация о боте Rinoku Bot", url="https://discord.gg/GND9y4e",
                         icon_url="https://cdn.discordapp.com/avatars/622747295435456512/a_a89ab431f88e458f51c4cd5fcf62bebf.gif?size=1024")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/706600733931339806/d64ac666b6dd26d6b156fb01c4628510.webp?size=1024")
        embed.add_field(name="Мои создатели:", value="NeloExt3#3100, don#4170, KislBall#9017", inline=False)
        embed.add_field(name="Моя ОС на:", value="Python, MongoDB", inline=True)
        embed.add_field(name="Версия:", value="Версия: 2 | Патч: 1", inline=True)

        embed.add_field(name="Я нахожусь на:", value=f"{servers} серверах!", inline=False)
        embed.add_field(name="Сервер технической поддержки", value="https://discord.gg/GND9y4e", inline=False)
        embed.add_field(name="Сайт бота", value="https://rinokubot.space", inline=False)
        embed.set_footer(text="Rinuku Bot | Все права были зашифрованны в двоичный код")

        await ctx.send(embed=embed)

    @commands.command()
    async def server(self, ctx):
        members = ctx.guild.members
        online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
        offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
        idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
        dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
        allchannels = len(ctx.guild.channels)
        allvoice = len(ctx.guild.voice_channels)
        alltext = len(ctx.guild.text_channels)
        allroles = len(ctx.guild.roles)
        embed=discord.Embed(
            title=f"{ctx.guild.name}",
            color=config.color
        )
        embed.add_field(name=f"Участники [{ctx.guild.member_count}]",
                        value=f"<:bot:728682548347011203>Ботов: **{len([m for m in members if m.bot])}**\n<:online:728682549819473970> Онлайн: **{online}**\n<:offline:728682548280033281> Офлайн: **{offline}** \n <:idle:728682549890515094> Отошли: **{idle}** \n<:dnd:728682911057838140>Не беспокоить: **{dnd}** \n",
                        inline=True)
        embed.add_field(name=f"Общее количество каналов [{allchannels}]", value=f"Текстовых каналов: {alltext}\nГолосовых каналов: {allvoice}", inline=True)
        embed.add_field(name="Создатель сервера", value=f"{ctx.guild.owner}", inline=False)
        embed.add_field(name=f"Информация о сервере", value=f"Сервер создан {ctx.guild.created_at.strftime('%A, %b %#d %Y')}\nРегион {ctx.guild.region}", inline=False)
        embed.set_footer(text=f"ID: {ctx.guild.id}", icon_url=ctx.guild.icon_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(utilites(client))
