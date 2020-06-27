# Импорт
import discord  # Discord
from discord.ext import commands  # Discord
import time
import random
import pymongo
import asyncio
import config

# <!-- DB Data -->
user = config.db_user
password = config.db_password
name = config.db_name

# Код
class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cog_name = ["Модерирование"]

    @commands.command(
        aliases=["пред", "варн"],
        description="Выдать предупреждение пользователю")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member = None, *, reason=None):
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]
        cursor = db[f"members_warns"]
        ids = 0

        for i in cursor.find({"guild": f"{message.guild.id}"}).sort("id", -1):
            if not i["id"]:
                ids = 1
                break
            else:
                ids = i["id"] + 1
                break

        cursor.insert_one(
            {"id": ids, "guild": f"{message.guild.id}", "member": f"{member.id}", "moderator": f"{moderator}","reason": f"{reason}"})

        await ctx.send(f"Предупреждение пользователю {member.display_name} с причиной {reason} успешно выдано! (ID предупреждения - `{number}`)")

    @commands.command(
        aliases=["убратьпред", "убратьварн"],
        description="Забрать предупреждение у пользовател через ID предупреждения")
    @commands.has_permissions(kick_members=True)
    async def unwarn(self, ctx, ids: int):
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]
        cursor = db[f"members_warns"]

        cursor.delete_one({"guild": f"{message.guild.id}", "id": ids})
        await ctx.send(f"Предупреждение пользователю {member.display_name} успешно убрано!")

    @commands.command(
        aliases=["преды", "варны"],
        description="Посмотреть предупреждения пользователя")
    @commands.has_permissions(kick_members=True)
    async def warns(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author

        warn_list = []

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]
        cursor = db[f"members_warns"]

        cursor.find({"guild": f"{message.guild.id}", "user": f"{member.id}"}).sort("id", -1)

        for i in warns:
            moder = ctx.guild.get_member(int(i['moderator']))
            warn_list.append(f"`ID - {i['id']}` | Выдал - {moder.display_name} | Причина - {i['reason']}\n")

        if not warn_list:
            warn_list = ["Пользователь не имеет предупреждений"]

        embed = discord.Embed(title=f"Предупреждения | {member.display_name}", description="".join(warn_list))
        embed.set_footer(text=config.copy, icon_url=config.icon)

        await ctx.send(embed=embed)

# <!-- Бан -->
    @commands.command(aliases=["Бан", "бан", "Ban"])
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
    @commands.command(aliases=["Разбан", "разбан", "Unban"])
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

    @commands.command(aliases=["очистить", "очистка", "клир"])
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
                embed=discord.Embed(description=f'❗️ {ctx.author.name},обязательно кол-во сообщений!'))

    # <!-- Кик -->
    @commands.command(aliases=["кик", "Кик", "Kick"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]
        cursor = db[f"guild_settings_logs"]

        logs_channel_id = cursor.find_one({"guild_id": f"{ctx.guild.id}"})
        if not logs_channel_id:
            return

        if member == ctx.message.author:
            return await ctx.send("Ты не можешь кикнуть сам себя.")

        msgg = f'Пользователь : {member.mention}, кикнут по причине : {reason}.'
        msgdm = f'Вы были забанены на сервере {ctx.guild.name}, по причине : {reason}.'

        if not reason:
            msgdm = f'Вы были кикнуты с сервера : {ctx.guild.name}.'
            msgg = f'Пользователь : {member.mention}, кикнут.'
            reason = "Не указанна"

        log_embed=discord.Embed(title="Участник был кикнут!", color=config.color)
        log_embed.add_field(name=f"Модератор: {ctx.author.name}", value=f"По причине `{reason}`", inline=False)

        await member.kick(reason=f"[RB]: Модератор {ctx.author.name}, по причине {reason}")
        await logs_channel.send(embed=log_embed)
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
