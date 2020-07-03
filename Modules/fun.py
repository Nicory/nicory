# Импорты
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


    @commands.command(
        aliases=[
            "Cry"
        ]
    )
    async def cry(self, ctx):
        gifs = [
            "https://media.giphy.com/media/ROF8OQvDmxytW/giphy.gif",
            "https://media.giphy.com/media/Ui7MfO6OaLz4k/giphy.gif",
            "https://media.giphy.com/media/Xqlsn2kLPBquI/giphy.gif",
            "https://media1.tenor.com/images/98466bf4ae57b70548f19863ca7ea2b4/tenor.gif?itemid=14682297"
        ]

        r_gif = random.choice(gifs)

        cry_embed = discord.Embed(description=f"{ctx.author.mention} плачет")
        cry_embed.set_image(url=r_gif)

        await ctx.send(embed=cry_embed)


@commands.command(
        aliases=[
            "Полиция",
            "полиция",
            "Police"
        ]
    )
    async def police(self, ctx, member: discord.Member):

        if member == ctx.message.author:
            return await ctx.send("Прости, но ты не можешь вызвать полицию на самого себя...")

        bot_id = 706600733931339806

        if member.id == bot_id:
            return await ctx.send("Извини, но я не позволю тебе вызвать полицию на меня.")
        if member.id == ctx.guild.owner.id:
            return await ctx.send("Ты не можешь вызвать полицию на создателя сервера.")
        if member.id == 622747295435456512:
            return await ctx.send(f"`Ошибка:` Юзер {member.name} находится под федеральной защитой США.")
        if member.id == 513287323836743680:
            return await ctx.send(f"`Ошибка:` Юзер {member.name} находится под федеральной защитой США.")

        gifs = [
            "https://i.gifer.com/MdNG.gif",
            "https://media.giphy.com/media/3oFzmlp7NUvDozVPmU/giphy.gif",
            "https://media.giphy.com/media/3osBLaQjYdcuVYpgXu/giphy.gif",
            "https://media.giphy.com/media/7zSO56YSB0DhNvBUWt/giphy.gif",
            "https://media.giphy.com/media/3dkPQ9JnxxQnVVMdOl/giphy.gif",
            "https://media.giphy.com/media/3dkPQ9JnxxQnVVMdOl/giphy.gif"
        ]

        r_gif = random.choice(gifs)

        swat_embed = discord.Embed(
            description=f"{ctx.author.mention} вызвал отряд полиции к {member.mention}",
        )
        swat_embed.set_image(url=r_gif)

        await ctx.send(embed=swat_embed)


    @commands.command(
        aliases=[
            "Погладить",
            "погладить",
            "Caress"
        ]
    )
    async def caress(self, ctx, member: discord.Member):
        if member == ctx.message.author:
            return await ctx.send("Прости, но ты не можешь погладить самого себя...")

        bot_id = 706600733931339806

        if member.id == bot_id:
            return await ctx.send("Извини, но ты не можешь погладить меня!")

        else:
            gifs = [
                "https://media1.tenor.com/images/ec064ff8e1b16e15080da778b7c032bc/tenor.gif",
                "https://pa1.narvii.com/6160/6ba8aa3c0a125492e5bce17972e835510bcd5cf7_hq.gif",
                "https://media1.tenor.com/images/0d7d8cce3aeca1b118da14cfc8668d2a/tenor.gif"
            ]

            r_gif = random.choice(gifs)

            caress_embed = discord.Embed(
                description=f"{ctx.author.mention} погладил {member.mention}",
            )
            caress_embed.set_image(url=r_gif)

            await ctx.send(embed=caress_embed)




def setup(client):
    client.add_cog(Fun(client))
