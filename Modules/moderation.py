# Импорт
import time
import discord  # Discord
import random
from discord.ext import commands  # Discord
import pymongo
import asyncio



# Код
class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # БАН

    @commands.command(aliases=["Бан", "бан", "Ban"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        if member == ctx.message.author:
            return await ctx.send("Ты не можешь забанить сам себя.")

        msgg = f'Пользователь : {member.mention}, забанен по причине : {reason}.'
        msgdm = f'Вы были забанены на сервере {ctx.guild.name}, по причине : {reason}.'

        if not reason:
            msgdm = f'Вы были забанены на сервере : {ctx.guild.name}.'
            msgg = f'Пользователь : {member.mention}, забанен.'

        await member.ban(reason=reason)
        await ctx.send(msgg)
        await member.send(msgdm)

    # РАЗБАН

    @commands.command(
        aliases=[
            "Разбан",
            "разбан",
            "Unban"
        ])
    @commands.has_permissions(
        ban_members=True
    )
    async def unban(self, ctx, member: discord.Member):
        await member.unban()
        await ctx.send(f'Пользователь : {member}, разбанен.')
        await member.send(f'Вы были разбанены на сервере : {ctx.guild.name}')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description=f':exclamation: {ctx.author.name},у вас нет прав для использования данной команды.',
                color=0x0c0c0c))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=discord.Embed(description=f':grey_exclamation: {ctx.author.name},обязательно укажите юзера'))

    # ОЧИСТКА ЧАТА

    @commands.command(
        aliases=[
            "очистить",
            "очистка",
            "клир"
        ])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):

        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send(embed=discord.Embed(
            description=f'**:heavy_check_mark: Удалено {amount} сообщений.**',
            color=0x800080),
            delete_after=3
        )

    # Работа с ошибками очистки чата

    @clear.error
    async def clear_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f'**:grey_exclamation: {ctx.author.name},обязательно укажите количевство сообщений.**',
                color=0x0c0c0c)
            )

    @commands.command(
        aliases=[
            "кик",
            "Кик",
            "Kick"
        ])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)

        await member.kick(reason=reason)
        await ctx.send(f'Пользователь {member.mention} был кикнут ')

        emb = discord.Embed(title="Информация о кике", description=f'{member.name.title()}, был кикнут', color=0x800080)
        emb.set_author(name=member, icon_url=member.avatar_ulr)

        await ctx.send(embed=emb)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=discord.Embed(description=f':grey_exclamation: {ctx.author.name},обязательно укажите юзера'))



def setup(client):
    client.add_cog(moderation(client))
