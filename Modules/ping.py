# Импорт
# <!-- Дискорд -->
import discord
from discord.ext import commands
import config
import pymongo

# <!-- DB Data -->
user = config.db_user
password = config.db_password
name = config.db_name

# Код
class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def ping(self, ctx, arg):
        await ctx.send(f"Pong!\n{arg}")


def setup(client):
    client.add_cog(ping(client))
