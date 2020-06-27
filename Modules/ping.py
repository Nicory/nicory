# Импорт
# <!-- Дискорд -->
import discord
from discord.ext import commands


# Код
class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")


def setup(client):
    client.add_cog(ping(client))
