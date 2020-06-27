import discord
from discord.ext import commands

class Fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  async def google(self, ctx, *, arg):
    escaped = "+".join(arg.split(" "))

    await ctx.send(f"Гугли, мой друг: https://google.gik-team.com?q={escaped}")

def setup(client):
    client.add_cog(Fun(client))
