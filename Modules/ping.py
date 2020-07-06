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




def setup(client):
    client.add_cog(ping(client))
