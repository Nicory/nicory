import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
      self.cog_name = ["Веселости"]

    @commands.command(aliases=["гугл"],description="Помоги пофиксить человеку баг, его код будет работать, научи его гуглить, его код будет работать всегда")
    async def google(self, ctx, *, arg):
        escaped = "+".join(arg.split(" "))

        await ctx.send(f"Я сгенерировала ссылку по вашему запросу:\nhttps://google.gik-team.com?q={escaped}")

    @commands.command(aliases=["обнять", "Обнять", "Hug"], description="Что может быть лучше чем обнимашки?")
    async def hug(self, ctx, member: discord.Member):

        if member == ctx.message.author:
            return await ctx.send("Прости, но ты не можешь обнять сам себя...")

        if member.id == self.bot.user.id:
            return await ctx.send("Извини, но я не разрешу обнимать себя >:c...")

        gifs = [
            "https://i.gifer.com/WDf.gif",
            "https://i.gifer.com/GAMC.gif",
            "https://66.media.tumblr.com/291c8b98b219283f9e21927e7ef6c3f2/tumblr_mzscklfLYx1tptsy9o1_500.gifv",
            "https://i.imgur.com/ntqYLGl.gif",
            "https://media1.tenor.com/images/af76e9a0652575b414251b6490509a36/tenor.gif?itemid=5640885",
            "https://media1.tenor.com/images/d3dca2dec335e5707e668b2f9813fde5/tenor.gif?itemid=12668677",
            "https://media1.tenor.com/images/155d024b04fe25f967eeef21adc5e4f0/tenor.gif?itemid=14625443",
            "https://media1.tenor.com/images/4f2158f495fa4a0cf80e38605dfe81e0/tenor.gif?itemid=16121369"
        ]


        r_gif = random.choice(gifs)

        hug_embed = discord.Embed(description=f"{ctx.author.mention} обнял {member.mention}")
        hug_embed.set_image(url=r_gif)

        await ctx.send(embed=hug_embed)



def setup(client):
    client.add_cog(Fun(client))
