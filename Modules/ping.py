# Импорт
# <!-- Дискорд -->
import discord
from discord.ext import commands
import config
import pymongo

# Код
class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cog_name = ["что-то", "Второй элемент в списке == ког не виден в хелпе"]

    @commands.command()
    async def ping(self, ctx, arg = None):
        if arg is None:
            await ctx.send("Pong! [Аргумент не был указан]")
        else:
            await ctx.send(f"Pong!\n{arg}")


def setup(client):
    client.add_cog(ping(client))
