import random
import discord
import config
import pymongo
from discord.ext import commands
from discord.utils import get


class levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cog_name = ["Система Уровней"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if not message.guild:
            return

        if len(message.content) > 5:
            conn = pymongo.MongoClient(config.MONGODB)
            db = conn[f"RB_DB"]  # Подключаемся к нужно БД
            cursor = db[f"members_levels"]  # Подключаемся к нужной колекции в нужной бд

            member = cursor.find_one({"guild": f"{message.guild.id}", "member": f"{message.author.id}"})

            if not member:
                cursor.insert_one({
                        "guild": f"{message.guild.id}",
                        "member": f"{message.author.id}",
                        "nickname": f"{message.author.name}",
                        "lvl": 1,
                        "xp": 0})

            member = cursor.find_one({"guild": f"{message.guild.id}", "member": f"{message.author.id}"})
            lvl = member["lvl"]
            xp = member["xp"]

            new_xp = xp + random.randint(20, 25)

            cursor.update_one({"guild": f"{message.guild.id}", "member": f"{message.author.id}"}, {'$set': {"xp": new_xp}})

            if new_xp >= lvl * 1000:
                embed=discord.Embed(description=f"{message.author.mention}\nПоздравляю, Ты получил новый уровень!\nТеперь твой уровень: {int(lvl + 1)}!", color=config.color)
                await message.channel.send(embed=embed)
                cursor.update_one({"guild": f"{message.guild.id}", "member": f"{message.author.id}"}, {'$set': {"lvl": int(lvl + 1)}})

    @commands.command(
        aliases=[
            "ранг",
            "ранк",
        ],
        description="Посмотреть свой уровень"
    )
    async def rank(self, ctx, member: discord.Member = None):
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_levels"]  # Подключаемся к нужной колекции в нужной бд

        if member is None:
            member = ctx.author

        info = cursor.find_one(
            {
                "guild": f"{ctx.guild.id}",
                "member": f"{member.id}"
            }
        )

        if not info:
            return await ctx.send(f"{ctx.author.mention}, я не обнаружила данного юзера в базе данных.")

        embed = discord.Embed(
            title=f"Ранг пользователя {member.display_name}",
            description=f"Уровень - {info['lvl']}\n"
                        f"Опыт - {info['xp']}/{int(info['lvl'])*1000}",
            color=config.color
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["рейтинг", "rating", "топ", "юзеры"],
        description="Рейтинг пользователей")
    async def exp_top(self, ctx):
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_levels"]  # Подключаемся к нужной колекции в нужной бд

        member = cursor.find({"guild": f"{ctx.guild.id}"}).sort([("xp", -1)])

        embed = discord.Embed(title="Рейтинг Пользователей", color=config.color)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        counter = 0

        for i in member:
            uid = i["member"]
            lvlu = i["lvl"]
            xp = i["xp"]

            if counter == 10:
                break

            usr = self.bot.get_user(int(uid))

            if not usr:
                pass
            else:
                counter += 1
                if counter == 1:
                    message = f":first_place: {usr.display_name}"
                elif counter == 2:
                    message = f":second_place: {usr.display_name}"
                elif counter == 3:
                    message = f":third_place: {usr.display_name}"
                else:
                    message = f"**#{counter}.** {usr.display_name}"

                try:
                    embed.add_field(name=message,
                                    value=f'**Уровень:** {lvlu} | **Опыт:** {xp}', inline=False)
                except Exception as e:
                    print("[ERROR] В рейтинге произошла следующая проблема:")
                    print(e)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(levels(client))
