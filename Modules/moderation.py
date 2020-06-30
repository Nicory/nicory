# Импорт
import discord  # Discord
from discord.ext import commands  # Discord
import time
import random
import pymongo
import asyncio
import config


# Код
class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cog_name = ["Модерирование"]

    @commands.command(
        aliases=["мьют", "мут", "Мут", "Мьют", "Mute"],
        description="Дать мьют пользователю")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, timenumber: int, typetime):
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_mute"]  # Подключаемся к нужной колекции в нужной бд

        timed = 0

        if typetime == "s" or typetime == "сек" or typetime == "секунд":
            timed = timenumber
        elif typetime == "m" or typetime == "мин" or typetime == "минут":
            timed = timenumber * 60
        elif typetime == "h" or typetime == "час" or typetime == "часов":
            timed = timenumber * 60 * 60
        elif typetime == "d" or typetime == "день" or typetime == "дней":
            timed = timenumber * 60 * 60 * 24

        times = time.time()
        times += timed

        mute_role = discord.utils.get(ctx.message.guild.roles, name="RB_Muted")

        if not mute_role:
            mute_role = await ctx.guild.create_role(name="RB_Muted")

        if mute_role in member.roles:
            await ctx.send(embed=discord.Embed(description=f'**:warning: Пользователь {member.mention} уже замьючен!**',
                                               color=config.error_color))
        else:
            i = cursor.find_one({"guild": f"{ctx.guild.id}", "id": f"{member.id}"})
            if i is None:
                cursor.insert_one({"guild": f"{ctx.guild.id}", "id": f"{member.id}", "mute": 0})

            cursor.update({"guild": f"{ctx.guild.id}", "id": f"{member.id}"}, {'$set': {"mute": times}})

            await member.add_roles(mute_role,
                                   reason=f"Пользователь {ctx.author.display_name} выдал мьют на {timenumber} {typetime}",
                                   atomic=True)
            await ctx.send(
                embed=discord.Embed(description=f'**:shield: Мьют пользователю {member.mention} успешно выдан!**',
                                    color=config.color))

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f'**:grey_exclamation: {ctx.author.name}, обязательно укажите юзера и время!**\n+мьют <юзер> <время> <тип времени>',
                color=config.error_color))

    # Размьют
    @commands.command(
        aliases=["размьют", "размут", "Размут", "Разьют", "Unmute"],
        description="снять мьют у пользователя")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_mute"]  # Подключаемся к нужной колекции в нужной бд

        i = cursor.find_one({"id": f"{ctx.author.id}", "guild": f"{ctx.guild.id}"})
        if i:
            mutes = i
        else:
            cursor.insert_one({"guild": f"{ctx.guild.id}", "id": f"{ctx.author.id}", "mute": 0})
            mutes = cursor.find_one({"id": f"{ctx.author.id}", "guild": f"{ctx.guild.id}"})

        mute = mutes["mute"]

        mute_role = discord.utils.get(ctx.message.guild.roles, name="Mute")

        if mute != 0:
            i = cursor.find_one({"guild": f"{ctx.guild.id}", "id": f"{member.id}"})
            if i is None:
                cursor.insert_one({"guild": f"{ctx.guild.id}", "id": f"{member.id}", "mute": 0})

            cursor.update({"guild": f"{ctx.guild.id}", "id": f"{member.id}"}, {'$set': {"mute": 0}})

            await member.remove_roles(mute_role)
            await ctx.send(embed=discord.Embed(
                description=f'**:white_check_mark: Мьют у пользователя {member.mention} Успешно снят! **',
                color=config.color))
        else:
            await ctx.send(
                embed=discord.Embed(description=f'**:warning: Пользователь {member.mention} Не замьючен!**',
                                    color=config.error_color))

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f'**:grey_exclamation: {ctx.author.name}, обязательно укажите юзера!**\n+размьют <юзер>',
                color=0x0c0c0c))

    @commands.command(
        aliases=["Пред", "пред", "Варн", "варн", "Warn"],
        description="Выдать предупреждение юзеру")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, arg):

        # Конект БД
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_warns"]  # Подключаемся к нужной колекции в нужной бд
        cursor_max = db[f"guild_settings_max_warns"]

        max_warns = cursor_max.find_one(
            {
                "guild": f"{ctx.guild.id}"
            }
        )

        if not max_warns:
            pass

        for i in cursor.find({"guild": f"{ctx.message.guild.id}"}).sort("id", -1):
            if not i["id"]:
                ids = 1
                break

            else:
                ids = i["id"] + 1
                break
        cursor.insert_one({"guild": f"{ctx.guild.id}", "moderator": f"{ctx.author.name}", "member": f"{member.id}", "reason": arg, "id": ids})

        if max_warns is not None:
            warns_number = cursor.find({"guild": f"{ctx.guild.id}", "member": f"{member.id}"})
            if not warns_number:
                return
            max_warns = int(max_warns['max_warns'])
            ban_warns = warns_number.count()
            if max_warns == ban_warns:
                await member.ban(reason='[Rinoku Bot]: Было превышено макс кол-во варнов')
                cursor.delete_many({"guild": f"{ctx.guild.id}", "member": f"{member.id}"})
                warn_embed = discord.Embed(
                    description=f"Было превышено максимальное количество варнов, я забанила данного юзера",
                    color=config.color
                )

                warn_embed.set_footer(
                    text='Rinuku Bot | Все права были зашифрованны в двоичный код',
                    icon_url=self.bot.user.avatar_url
                )

                warn_embed_d = discord.Embed(
                    description=f"Вы были забанены на сервере `{ctx.guild.name}` по причине: `Было превышено максимальное количество варнов`",
                    color=config.color
                )

                warn_embed_d.set_footer(
                    text='Rinuku Bot | Все права были зашифрованны в двоичный код',
                    icon_url=self.bot.user.avatar_url
                )

                await ctx.send(embed=warn_embed)
                await member.send(embed=warn_embed_d)

        cursor.insert_one(
            {"id": ids, "guild": f"{ctx.message.guild.id}", "member": f"{member.id}", "moderator": f"{ctx.author.id}","reason": f"{arg}"})

        await ctx.send(f"Предупреждение пользователю {member.display_name} с причиной {arg} успешно выдано! (ID предупреждения - `{ids}`)")

    @commands.command(
        aliases=[
            "CнятьВарн",
            "снятьВарн",
            "Снятьварн",
            "снятьварн",
            "Unwarn"
        ],
        description="Снять варн юзеру [Для снятие варна используйте уникальный ID варна]"
    )
    @commands.has_permissions(
        kick_members=True
    )
    async def unwarn(self, ctx, ids: int):

        # Конект БД
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_warns"]  # Подключаемся к нужной колекции в нужной бд

        cursor.delete_one({"guild": f"{ctx.message.guild.id}", "id": ids})
        await ctx.send(f"Предупреждение под номером `{ids}` успешно убрано!")

        unwarn_embed = discord.Embed(
            description=f"Варн, уникальный номер которого:`{ids}` был успешно снят!",
            color=config.color
        )

        unwarn_embed.set_footer(
            text='Rinuku Bot | Все права были зашифрованны в двоичный код',
            icon_url=self.bot.user.avatar_url
        )
        await ctx.send(embed=unwarn_embed)

    @unwarn.error
    async def unwarn_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f'❗️ {ctx.author.name},обязательно укажите уникальный номер варна!',
                color=config.error_color))

    @commands.command(
        aliases=[
            "Варны",
            "варны",
            "Преды",
            "преды",
            "Warns"
        ],
        description="Просмотреть варны юзера"
    )
    async def warns(self, ctx, member: discord.Member=None):
        # Конект БД
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_warns"]  # Подключаемся к нужной колекции в нужной бд

        if not member:
            member = ctx.author

        a = []

        for i in cursor.find({"guild": f"{ctx.guild.id}", "member": f"{member.id}"}).sort("id", -1):
            a.append(f"`ID - {i['id']}` | Модератор - {i['moderator']} | Причина - {i['reason']}\n")

        if not a:
            a = ["Юзер не имеет варнов"]
        embed = discord.Embed(
            title=f"Варны {member.display_name}",
            description="".join(a),
            color=config.color
        )

        embed.set_footer(
            text='Rinuku Bot | Все права были зашифрованны в двоичный код',
            icon_url=self.bot.user.avatar_url
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

# <!-- Бан -->
    @commands.command(aliases=["Бан", "бан", "Ban"], description="Забанить юзера")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]
        cursor = db[f"guild_settings_logs"]

        if member == ctx.message.author:
            return await ctx.send("Ты не можешь забанить сам себя.")

        msgg = f'Пользователь: {member.mention}, забанен по причине: `{reason}`.'
        msgdm = f'Вы были забанены на сервере {ctx.guild.name}, по причине: `{reason}`.'

        if not reason:
            msgdm = f'Вы были забанены на сервере : {ctx.guild.name}.'
            msgg = f'Пользователь: {member.mention}, забанен.'
            reason = "Не указанна"

        logs_channel_id = cursor.find_one({"guild_id": f"{ctx.guild.id}"})
        if not logs_channel_id:
            return

        else:
            logs_channel=self.bot.get_channel(int(logs_channel_id["channel_id"]))
            log_embed=discord.Embed(title=f"❗️Участник {member.name} был забанен!", color=config.color)
            log_embed.add_field(name=f"Модератор: {ctx.author.name}", value=f"По причине `{reason}`", inline=False)
            await logs_channel.send(embed=log_embed)

        await member.ban(reason=f"[RB]: Модератор {ctx.author.name}, по причине {reason}")
        await ctx.send(msgg)
        await member.send(msgdm)

# <!-- Разбан -->
    @commands.command(aliases=["Разбан", "разбан", "Unban"], description="Разбанить юзера")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]
        cursor = db[f"guild_settings_logs"]

        logs_channel_id = cursor.find_one({"guild_id": f"{ctx.guild.id}"})
        if not logs_channel_id:
            return

        else:
            logs_channel=self.bot.get_channel(int(logs_channel_id["channel"]))
            log_embed=discord.Embed(title="Участник был разбанен!", color=config.color)
            log_embed.add_field(name=f"Модератором {ctx.author.name}", value=f"", inline=False)
            await logs_channel.send(embed=log_embed)

        await member.unban()
        await ctx.send(f'Пользователь : {member.name}, разбанен.')
        await member.send(f'Вы были разбанены на сервере : {ctx.guild.name}')

# <!-- Обработка ошибок бана -->
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=discord.Embed(description=f'❗️ {ctx.author.name},обязательно укажите юзера'))

    # ОЧИСТКА ЧАТА

    @commands.command(aliases=["очистить", "очистка", "клир"], description="Очистить чат")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send(embed=discord.Embed(
            description=f'**❗️ Удалено {amount} сообщений.**',
            color=config.color),
            delete_after=3
        )

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=discord.Embed(description=f'❗️ {ctx.author.name},обязательно кол-во сообщений!', color=config.error_color))

    # <!-- Кик -->
    @commands.command(aliases=["кик", "Кик", "Kick"], description="Кикнуть юзера")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]
        cursor = db[f"guild_settings_logs"]

        # logs_channel_id = cursor.find_one({"guild_id": f"{ctx.guild.id}"})
        # if not logs_channel_id:
        #    return

        if member == ctx.message.author:
            return await ctx.send("Ты не можешь кикнуть сам себя.")

        msgg = f'Пользователь : {member.mention}, кикнут по причине : {reason}.'
        msgdm = f'Вы были забанены на сервере {ctx.guild.name}, по причине : {reason}.'

        if not reason:
            msgdm = f'Вы были кикнуты с сервера : {ctx.guild.name}.'
            msgg = f'Пользователь : {member.mention}, кикнут.'
            reason = "Не указанна"

        # log_embed=discord.Embed(title="Участник был кикнут!", color=config.color)
        # log_embed.add_field(name=f"Модератор: {ctx.author.name}", value=f"По причине `{reason}`", inline=False)

        await member.kick(reason=f"[RB]: Модератор {ctx.author.name}, по причине {reason}")
        # await logs_channel.send(embed=log_embed)
        await ctx.send(msgg)
        await member.send(msgdm)

# <!-- Обработка ошибок кика -->
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=discord.Embed(description=f'❗️ {ctx.author.name},обязательно укажите юзера'))

# <!-- Репорты -->
    @commands.command(
        aliases=["Тикет", "тикет", "репорт", "Репорт"],
        description="Написать жалобу на юзера"    )
    async def ticket(self, ctx):
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]
        cursor = db[f"guild_settings_reports"]
        prefix = db["guild_settings_prefixes "].find_one({"guild": f"{ctx.guild.id}"})
        if prefix is None:
            prefix = "!!"
        else:
            prefix = prefix["prefix"]

        author = ctx.message.author.name
        author = author.lower()
        author = author.replace(" ", "-")
        guild = ctx.message.guild
        authorTag = ctx.message.author

        color = config.color  # Цвет полоски

        ticketc = f'репорт-{author}'

        reportc = cursor.find_one({"guild": f"{ctx.guild.id}"})["channel"]

        if reportc == 0 or reportc is None:
            await ctx.send(f"{ctx.author.mention}, администрация не указала канал для тикетов!")

        else:
            reportc = int(reportc)

            llist = []
            for i in ctx.message.guild.channels:
                llist.append(i.name)

            if ticketc in llist:
                await ctx.send(f"У вас уже открыт репорт, напишите {prefix}`закрытьтикет` чтобы закрыть тикет")
            else:
                await ctx.message.delete()
                await ctx.send("Репорт успешно создан!", delete_after=10)

                creport = discord.utils.get(ctx.message.guild.categories, id=reportc)
                channel = await guild.create_text_channel(f'репорт-{author}', overwrites=None, category=creport,
                                                          reason=f'Создан репорт для {author}')

                await channel.set_permissions(authorTag, read_messages=True, send_messages=True)

                emb = discord.Embed(title=f"Тикет Пользователя {authorTag.display_name}",
                                    description="Здравствуйте! \n Для решения Вашей проблемы мы создали отдельный чат "
                                                "с модерацией сервера! \n \n Опишите Вашу проблему полностью и "
                                                "развёрнуто и модерация сервера ответит Вам. \n \n Старайтесь "
                                                "описывать проблему доступным для понимания текстом.",
                                    color=color)
                emb.add_field(name="Закрыть тикет", value=f"`{prefix}закрытьтикет`")
                emb.add_field(name="Добавить пользователя в тикет", value=f"`{prefix}добавитьтикет`")
                emb.set_footer(text=config.copy, icon_url=config.icon)

                await channel.send(authorTag.mention)
                await channel.send(embed=emb)

    @commands.command(
        aliases=['закрытьтикет', 'closeticket', 'закрыть', 'закрытьрепорт'],
        description="Закрыть репорт")
    async def closetickets(self, ctx):
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]
        cursor = db[f"guild_settings_reports"]
        reportc = cursor.find_one({"guild": f"{ctx.guild.id}"})["channel"]

        author = ctx.message.author.name
        author = author.lower()
        author = author.replace(" ", "-")

        if ctx.message.channel.category.id == int(reportc):
            await ctx.message.channel.delete(
                reason=f'Тикет закрыть пользователем - {ctx.message.author.display_name} ({ctx.author.name} {ctx.author.discriminator})')

        else:
            if ctx.message.channel.name == f"тикет-{author}":
                await ctx.message.channel.delete(
                    reason=f'Тикет закрыть пользователем - {ctx.message.author.display_name} ({ctx.author.name} {ctx.author.discriminator})')
            else:
                await ctx.send("Эта команда работает только в тикете!")

    @commands.command(
        aliases=['добавитьтикет', 'addticket', 'добавить', 'добавитьрепорт'],
        description="Добавить кого-то в репорт")
    async def addtickets(self, ctx, member: discord.Member):
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]
        cursor = db[f"guild_settings_reports"]
        reportc = cursor.find_one({"guild": f"{ctx.guild.id}"})["channel"]

        author = ctx.message.author.name
        author = author.lower()
        author = author.replace(" ", "-")

        if ctx.message.channel.category.id == int(reportc):
            await ctx.channel.set_permissions(member, read_messages=True, send_messages=True)
            await ctx.send(f"{member.mention} успешно добавлен в тикет!")
        else:
            if ctx.message.channel.name == f"тикет-{author}":
                await ctx.channel.set_permissions(member, read_messages=True, send_messages=True)
                await ctx.send(f"{member.mention} успешно добавлен в тикет!")
            else:
                await ctx.send("Эта команда работает только в тикете!")


def setup(client):
    client.add_cog(moderation(client))
