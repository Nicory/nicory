import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @commands.command()
    async def google(self, ctx, *, arg):
        escaped = "+".join(arg.split(" "))

        await ctx.send(f"Я сгенерировала ссылку по вашему запросу:\nhttps://google.gik-team.com?q={escaped}")

    @commands.command(aliases=["обнять", "Обнять", "Hug"])
    async def hug(self, ctx, member: discord.Member):

        if member == ctx.message.author:
            return await ctx.send("Прости, но ты не можешь обнять сам себя...")

        if member.id == self.bot.user.id:
            return await ctx.send("Извини, но я не разрешу обнимать себя >:c...")

        gifs = ["https://i.gifer.com/WDf.gif", "https://i.gifer.com/GAMC.gif", "https://acegif.com/wp-content/gif/anime-hug-38.gif"]

        r_gif = random.choice(gifs)

        hug_embed = discord.Embed(description=f"{ctx.author.mention} обнял {member.mention}")
        hug_embed.set_image(url=r_gif)

        await ctx.send(embed=hug_embed)



def setup(client):
    client.add_cog(Fun(client))
