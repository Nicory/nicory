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
        conn = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@rinoliku-2-qvq4c.mongodb.net/{name}?retryWrites=true&w=majority")
        db = conn[f"RB_DB"]
        cursor = db[f"guild_settings_logs"]
        cursor.insert_one({"guild_id": f"{ctx.guild.id}", "channel_id": arg})


def setup(client):
    client.add_cog(ping(client))
