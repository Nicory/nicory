# Импорт
# <!-- Дискорд -->
import discord
from discord.ext import commands
import Cybernator
from Cybernator import Paginator

# Код
class utilites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cog_name = ["Утилиты"]




def setup(client):
    client.add_cog(utilites(client))
