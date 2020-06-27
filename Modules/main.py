import discord
from discord.ext import commands
from pymongo import MongoClient
import config
import os
import string
import random

class Main(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def token(self, ctx):
    client = MongoClient(config.MONGODB)
    db = client['RB_DB']
    col = db['admin_tokens']

    token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(16))

    col.remove({
      'guild': ctx.guild.id,
      'member': ctx.author.id
    })

    col.insert_one({
      'guild': ctx.guild.id,
      'member': ctx.author.id,
      'token': token
    })

    await ctx.message.add_reaction('✅')
    await ctx.author.send(f'Ваш ключ доступа для {ctx.guild} - ||{token}||\nВсе ваши токены были обнулены')

  @token.error
  async def token_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.message.add_reaction('❌')



def setup(client):
    client.add_cog(Main(client))
