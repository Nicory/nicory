# Импорт
import discord  # Discord
from discord.ext import commands  # Discord
import pymongo
import config

# <!-- DB Data -->
user = config.db_user
password = config.db_password
name = config.db_name

# Код
class logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # Конект БД
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"guild_settings_logs"]  # Подключаемся к нужной колекции в нужной бд

        if message.guild:
            id = cursor.find_one({"guild_id": f"{message.guild.id}"})

        if not id:
            return

        if message.author.id == self.bot.user.id:
            return

        if message.author.bot:
            return

        else:
            channel = self.bot.get_channel(int(id["channel_id"]))
            logs_embed = discord.Embed(
                color=config.color
            )
            logs_embed.set_author(
                name="Сообщение было удалено!",
                icon_url=self.bot.user.avatar_url
            )
            logs_embed.add_field(name="Сообщение:", value=f"```{message.content}```", inline=False)
            logs_embed.add_field(name="Автор:", value=f"**{message.author}** | ({message.author.mention})", inline=True)
            logs_embed.add_field(name="Канал:", value=f"**{message.channel.name}** ({message.channel.mention})",
                                 inline=True)
            logs_embed.set_footer(text=f'Уникальный ID сообщения: {message.id}')
            await channel.send(embed=logs_embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # Конект БД
        global id
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"guild_settings_logs"]  # Подключаемся к нужной колекции в нужной бд

        if after.guild:
            id = cursor.find_one({"guild_id": f"{after.guild.id}"})

        if not id:
            return

        if after.author.id == self.bot.user.id:
            return

        if before.author.bot:
            return

        else:
            channel = self.bot.get_channel(int(id["channel_id"]))
            logs_embed = discord.Embed(
                color=config.color
            )
            logs_embed.set_author(
                name="Сообщение было отредактировано!",
                icon_url=self.bot.user.avatar_url
            )
            logs_embed.add_field(name="Старое сообщение:", value=f"```{before.content}```", inline=False)
            logs_embed.add_field(name="Новое сообщение:", value=f"```{after.content}```", inline=False)
            logs_embed.add_field(name="Автор:", value=f"**{after.author}** | ({after.author.mention})", inline=True)
            logs_embed.add_field(name="Канал:", value=f"**{after.channel.name}** ({after.channel.mention})",
                                 inline=True)
            logs_embed.set_footer(text=f'Уникальный ID сообщения: {after.id}')
            await channel.send(embed=logs_embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Конект БД
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"guild_settings_logs"]  # Подключаемся к нужной колекции в нужной бд

        if member.guild:
            id = cursor.find_one({"guild_id": f"{member.guild.id}"})

        if not id:
            return

        else:
            channel = self.bot.get_channel(int(id["channel_id"]))
            logs_embed = discord.Embed(
                color=config.color
            )
            logs_embed.set_author(
                name="С сервера ушёл человек!",
                icon_url=self.bot.user.avatar_url
            )
            logs_embed.add_field(name="Имя:", value=f"`{member.name}`", inline=False)
            logs_embed.add_field(name="ID:", value=f"`{member.id}`", inline=False)
            await channel.send(embed=logs_embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Конект БД
        global id
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"guild_settings_logs"]  # Подключаемся к нужной колекции в нужной бд

        if member.guild:
            id = cursor.find_one({"guild_id": f"{member.guild.id}"})

        if not id:
            return

        else:
            channel = self.bot.get_channel(int(id["channel_id"]))
            logs_embed = discord.Embed(
                color=config.color
            )
            logs_embed.set_author(
                name="На сервер зашёл человек!",
                icon_url=self.bot.user.avatar_url
            )
            logs_embed.add_field(name="Имя:", value=f"`{member.name}`", inline=False)
            logs_embed.add_field(name="ID:", value=f"`{member.id}`", inline=False)
            await channel.send(embed=logs_embed)


def setup(client):
    client.add_cog(logs(client))
