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
    aliases=["Пред", "пред", "Варн", "варн", "Warn"],
    description="Выдать предупреждение юзеру"
    )
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
            logs_channel=self.bot.get_channel(int(logs_channel_id["channel_id"]))
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



def setup(client):
    client.add_cog(moderation(client))
