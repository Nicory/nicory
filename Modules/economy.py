# Импорт
import discord  # Discord
from discord.ext import commands  # Discord
import random
import pymongo
from discord.utils import get
import config

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cog_name = ["Экономика"]

    @commands.Cog.listener()
    async def on_message(self, message):
        # Конект БД
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_economy"]  # Подключаемся к нужной колекции в нужной бд

        if message.guild:  # Проверка на сервере ли это
            user = cursor.find_one(
                {
                    "guild": f"{message.guild.id}",
                    "m_id": f"{message.author.id}"
                }
            )
        else:
            return

        if message.author.id == self.bot.user.id:
            return

        if not user:
            cursor.insert_one(
                {
                    "guild": f"{message.guild.id}",
                    "m_id": f"{message.author.id}",
                    "m_name": f"{message.author.name}",
                    "money": 0
                }
            )

        else:
            return

    @commands.command(
        aliases=[
            "баланс",
            "Баланс",
        ],
        description="Посмотреть свой баланс"
    )
    async def balance(self, ctx, member: discord.Member = None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_economy"]  # Подключаемся к нужной колекции в нужной бд

        if member is None:
            member = ctx.author

        bal = cursor.find_one(
            {
                "guild": f"{ctx.guild.id}",
                "m_id": f"{member.id}"
            }
        )

        if not bal:
            return await ctx.send(f"{ctx.author.mention}, я не обнаружила данного юзера в базе данных.")

        embed = discord.Embed(
            title=f"Баланс пользователя {member.name}",
            description=f"{bal['money']} Кредитов <:credit:726813969167155320>",
            color=config.color
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @balance.error
    async def bal_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=discord.Embed(description=f':grey_exclamation: {ctx.author.name},обязательно укажите юзера!'))

    @commands.command(
        aliases=[
            "выдать",
            "Выдать"
        ],
        description="Выдать пользователю деньги"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def award(self, ctx, member: discord.Member = None, amount: int = None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_economy"]  # Подключаемся к нужной колекции в нужной бд

        bal = cursor.find_one(
            {
                "guild": f"{ctx.guild.id}",
                "m_id": f"{member.id}"
            }
        )

        if not bal:
            return await ctx.send(f"{ctx.author.mention}, я не обнаружила данного юзера в базе данных.")

        if member is None:
            await ctx.send(f"{ctx.author.mention}, укажите юзера")

        if member.id == self.bot.user.id:
            return await ctx.send(f"Я ценю то, что вы пытаетесь мне дать денег, но простите, для безопасности системы я не могу принять их.")

        else:
            if amount is None:
                await ctx.send(f"{ctx.author.mention}, укажите сумму которую хотите зачислить участнику")

            if amount < 1:
                await ctx.send(f"{ctx.author.mention}, сумма зачисления не может быть ниже `1` кредита")

            else:
                mount = bal["money"] + amount
                if cursor.find_one({"guild": f"{ctx.guild.id}", "m_id": f"{member.id}"}):
                    cursor.update_one({"guild": f"{ctx.guild.id}", "m_id": f"{member.id}"}, {'$set': {"money": mount}})

                    emb = discord.Embed(
                        description=f"На баланс пользователя {member.mention} было зачисленно {amount} кредит(ов)!",
                        color=config.color
                    )

                    await ctx.send(embed=emb)
                else:
                    await ctx.send(f"{ctx.author.mention}, я не обнаружила данного юзера в базе данных.")

    @commands.command(
        aliases=[
            "забрать",
            "Забрать"
        ],
        description="Забрать у пользвателя деньги"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def take(self, ctx, member: discord.Member = None, amount: int = None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_economy"]  # Подключаемся к нужной колекции в нужной бд

        bal = cursor.find_one(
            {
                "guild": f"{ctx.guild.id}",
                "m_id": f"{member.id}"
            }
        )

        if not bal:
            return await ctx.send(f"{ctx.author.mention}, я не обнаружила данного юзера в базе данных.")

        balance = bal['money']

        if member is None:
            await ctx.send(f"{ctx.author.mention}, укажите юзера")

        if member.id == self.bot.user.id:
            return await ctx.send(f"Я понимаю что вы хотите отнять у меня деньги, но в целях безопасности системы этого сделать нельзя.")

        else:
            if amount is None:
                await ctx.send(f"{ctx.author.mention}, укажите сумму которую хотите отнять у участника")

            if amount > balance:
                return await ctx.send(f"{ctx.author.mention}, у юзера {member.mention} нету столько кредитов!")

            if amount < 1:
                await ctx.send(f"{ctx.author.mention}, сумма не может быть ниже `1` кредита")

            else:
                mount = bal["money"] - amount
                if cursor.find_one({"guild": f"{ctx.guild.id}", "m_id": f"{member.id}"}):
                    cursor.update_one({"m_id": f"{member.id}"}, {'$set': {"money": mount}})

                    emb = discord.Embed(
                        description=f"С баланса {member.mention} было снято {amount} кредита(ов)!",
                        color=config.color
                    )

                    await ctx.send(embed=emb)

    @commands.command(
        aliases=[
            "добавить-в-магазин",
        ],
        description="Добавить товар в магазин"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def add_shop(self, ctx, role: discord.Role = None, cost: int = None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"guild_shop"]  # Подключаемся к нужной колекции в нужной бд

        if role is None:
            await ctx.send(f"{ctx.author.mention}, укажите роль которую хотите внести в магазин!")
        else:
            if cost is None:
                await ctx.send(f"{ctx.author.mention}, укажите цену роли!")
            elif cost < 1:
                await ctx.send(f"{ctx.author.mention}, цена не может быть меньше `1` кредита!")
            else:
                cursor.insert_one(
                    {
                        "role_id": role.id,
                        "guild": ctx.guild.id,
                        "cost": cost
                    }
                )
                await ctx.message.add_reaction('✅')

    @commands.command(
        aliases=[
            "удалить-из-магазина"
        ],
        description="Удалить товар из магазина"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def remove_shop(self, ctx, role: discord.Role = None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"guild_shop"]  # Подключаемся к нужной колекции в нужной бд

        if role is None:
            await ctx.send(f"{ctx.author.mention}, укажите роль которую хотите удалить из магазина!")

        elif cursor.find_one({"role_id": role.id, "guild": ctx.guild.id}) is None:
            await ctx.send(f"{ctx.author.mention}, данной роли нету в магазине!")

        else:
            cursor.delete_one(
                {
                    "role_id": role.id,
                    "guild": ctx.guild.id
                }
            )
            await ctx.message.add_reaction('✅')

    @commands.command(
        aliases=[
            "магазин"
        ],
        description="Посмотреть товары в магазине"
    )
    async def shop(self, ctx):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"guild_shop"]  # Подключаемся к нужной колекции в нужной бд

        embed = discord.Embed(
            title="Магазин ролей",
            color=config.color
        )

        for i in cursor.find({"guild": ctx.guild.id}):
            if ctx.guild.get_role(i['role_id']) is not None:
                embed.add_field(
                    name=f"Роль {ctx.guild.get_role(i['role_id'])}",
                    value=f"Стоимость: {i['cost']} кредитов\n[{ctx.guild.get_role(i['role_id']).mention}]",
                    inline=False
                )

            else:
                return

        await ctx.send(embed=embed)

    @commands.command(
        aliases=[
            "купить"
        ],
        description="Купить Товар"
    )
    async def buy(self, ctx, role: discord.Role = None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor_s = db[f"shop"]  # Подключаемся к нужной колекции в нужной бд
        cursor_m = db[f"economy"]

        c = cursor_s.find_one(
            {
                "guild": ctx.guild.id,
                "role_id": role.id
            }
        )
        m = cursor_m.find_one(
            {
                "guild": f"{ctx.guild.id}",
                "m_id": f"{ctx.author.id}"
            }
        )
        cost = c['cost']

        money = m['money']

        if role is None:
            return await ctx.send(f"{ctx.author.mention}, укажите роль которую хотите купить.")
        else:
            if role in ctx.author.roles:
                return await ctx.send(f"{ctx.author.mention}, у вас уже имеется данная роль.")

            if cost > money:
                return await ctx.send(f"{ctx.author.mention}, у вас недостаточно кредитов для покупки этой роли!")

            else:
                await ctx.author.add_roles(role)
                await ctx.message.add_reaction('✅')
                mount = money - cost
                cursor_m.update_one({"m_id": f"{ctx.author.id}"}, {"guild:": f"{ctx.guild.id}"}, {'$set': {"money": mount}})

    @commands.command(
        aliases=[
            "продать"
        ],
        description="Купить Товар"
    )
    async def sell(self, ctx, role: discord.Role = None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor_s = db[f"shop"]  # Подключаемся к нужной колекции в нужной бд
        cursor_m = db[f"economy"]

        c = cursor_s.find_one({"guild": ctx.guild.id, "role_id": role.id})
        m = cursor_m.find_one({"guild": f"{ctx.guild.id}", "m_id": f"{ctx.author.id}"})
        cost = c['cost']

        money = m['money']

        if role is None:
            return await ctx.send(f"{ctx.author.mention}, укажите роль которую хотите купить.")
        else:
            if role not in ctx.author.roles:
                return await ctx.send(f"{ctx.author.mention}, у вас нету данной роли.")

            else:
                await ctx.author.add_roles(role)
                await ctx.message.add_reaction('✅')
                mount = money + cost
                cursor_m.update_one({"m_id": f"{ctx.author.id}", "guild:": f"{ctx.guild.id}"}, {'$set': {"money": mount}})

    @commands.command(
        aliases=[
            "работать",
            "Работать",
            "Работа",
            "работа"
        ],
        description="Работать чтобы заработать деньги"
    )
    @commands.cooldown(1, 1800, commands.BucketType.member)
    async def work(self, ctx, *, arg):
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_economy"]  # Подключаемся к нужной колекции в нужной бд
        cursor_guild_custom_works = db[f"guild_custom_works"]

        arg = arg.lower()

        custom_work = cursor_guild_custom_works.find({"guild": f"{ctx.guild.id}"})

        if not custom_work:
            return

        c_w = None
        min = None
        max = None

        for i in custom_work:
            c_w = i['work']
            print(c_w)
            min = i['min']
            max = i['max']

        good_work = [
            "кодер",
            "программист",
            "инженер",
            "хирург",
            "врач"
        ]
        medium_work = [
            "продавец"
        ]
        bad_work = [
            "грузчик",
            "дворник"
        ]
        m = 0
        if arg in good_work:
            m = random.randint(50, 600)
        elif arg in medium_work:
            m = random.randint(50, 400)
        elif arg in bad_work:
            m = random.randint(50, 200)

        elif arg in c_w:
            m = random.randint(min, max)

        elif arg not in good_work and arg not in medium_work and arg not in bad_work:

            if arg not in c_w:
                self.work.reset_cooldown(ctx)
                return await ctx.send(f"{ctx.author.mention}, я не обнаружила вашу работу ни в одном из списков, пропишите `!!работы` чтоб узнать список всех работ.")

            else:
                self.work.reset_cooldown(ctx)
                return await ctx.send(f"{ctx.author.mention}, я не обнаружила вашу работу ни в одном из списков, пропишите `!!работы` чтоб узнать список всех работ.")

        mon = cursor.find_one(
            {
                "guild": f"{ctx.guild.id}",
                "m_id": f"{ctx.author.id}"
            }
        )

        mount = mon["money"] + m
        cursor.update_one({"m_id": f"{ctx.author.id}", "guild": f"{ctx.guild.id}"}, {'$set': {"money": mount}})

        e = discord.Embed(
            description=f"{ctx.author.mention} работает на работе `{arg}`, и зарабатывает **{m}** кредита(ов)!",
            color=config.color
        )
        await ctx.send(embed=e)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=discord.Embed(
                    description=f':grey_exclamation: {ctx.author.name},обязательно укажите место работы!'))
            self.work.reset_cooldown(ctx)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed=discord.Embed(
                    description=f':grey_exclamation: {ctx.author.name}, подождите `{error.retry_after:.2f}` секунд для повторного использования команды!'))

    @commands.command(
        aliases=[
            "добавить-работу"
        ],
        description="Добавить свою работу"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def add_work(self, ctx, work, min: int, max: int):
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"custom_work"]  # Подключаемся к нужной колекции в нужной бд

        if not work and min and max:
            return await ctx.send(f"{ctx.author.mention}, команда добавление работы пишется так: `!!добавить-работу имя-работы минимальная-сумма-зароботка максимальная-сумма-зароботка`")

        cursor.insert_one(
            {
                "guild": f"{ctx.guild.id}",
                "work": f"{work}",
                "min": min,
                "max": max,
            }
        )

        await ctx.message.add_reaction('✅')

    @commands.command(
        aliases=[
            "удалить-работу"
        ],
        description="Удалить работу"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def remove_work(self, ctx, work):
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"guild_custom_works"]  # Подключаемся к нужной колекции в нужной бд

        if not work :
            return await ctx.send(f"{ctx.author.mention}, команда удаление работы пишется так: `!!удалить-работу имя-работы`.")

        cursor.delete_one(
            {
                "guild": f"{ctx.guild.id}",
                "work": f"{work}"
            }
        )

        await ctx.message.add_reaction('✅')

    @commands.command(
        aliases=[
            "Работы",
            "работы"
        ],
        description="Список работ"
    )
    async def works(self, ctx):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"custom_work"]  # Подключаемся к нужной колекции в нужной бд


        embed = discord.Embed(
            title="Список всех работ:",
            description=f"**Хорошие работы [Зарплата: 50-600]**\nКодер, Программист, Инженер, Врач, Хирург.\n**Средние работы [Зарплата: 50-400]**\nПродавец.\n**Плохие работы [Зарплата: 50-200]**\nГрузчик, Дворник.\n\nКастомные работы:",
            color=config.color
        )
        for i in cursor.find({"guild": f"{ctx.guild.id}"}):
            embed.add_field(
                name=f"Работа {i['work']}",
                value=f"Зарплата: {i['min']}-{i['max']} кредитов",
                inline=False
            )

        embed.set_footer(
            text='Rinuku Bot | Все права были зашифрованны в двоичный код',
            icon_url=self.bot.user.avatar_url
        )
        await ctx.send(embed=embed)

    @commands.command(
        aliases=[
            "Bet",
            "ставка",
            "Ставка"
        ],
        description="Сделать ставку"
    )
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def bet(self, ctx, amount: int = None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_economy"]  # Подключаемся к нужной колекции в нужной бд

        m = cursor.find_one(
            {
                "guild": f"{ctx.guild.id}",
                "m_id": f"{ctx.author.id}"
            }
        )

        money = m['money']

        if amount is None:
            self.bet.reset_cooldown(ctx)
            return await ctx.send(f"{ctx.author.mention}, укажите сколько денег хотите поставить")

        elif amount <= 0:
            return await ctx.send(f"{ctx.author.mention}, укажите количество больше 0")

        if amount > money:
            return await ctx.send(f"{ctx.author.mention}, у вас недостаточно кредитов для этого!")

        if random.randint(1, 2) == 1:
            mount = m["money"] - amount
            if cursor.find_one({"guild": f"{ctx.guild.id}", "m_id": f"{ctx.author.id}"}):
                cursor.update_one({"m_id": f"{ctx.author.id}"}, {'$set': {"money": mount}})

            await ctx.send(
                embed=discord.Embed(title="Проигрыш", color=config.color, description=f"Вы проиграли {amount} кредитов..."))

        elif random.randint(1, 2) == 2:
            d = amount * 2
            mount = m["money"] + d
            if cursor.find_one({"guild": f"{ctx.guild.id}", "m_id": f"{ctx.author.id}"}):
                cursor.update_one({"m_id": f"{ctx.author.id}"}, {'$set': {"money": mount}})

            await ctx.send(
                embed=discord.Embed(title="Победа", color=190090, description=f"Вы выиграли {amount * 2} кредитов"))

    @bet.error
    async def bet_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed=discord.Embed(
                    description=f':grey_exclamation: {ctx.author.name}, подождите `{error.retry_after:.2f}` секунд для повторного использования команды!'))

    @commands.command(
        aliases=[
            "Transfer",
            "перевести",
            "Перевести"
        ],
        description="Перевести другому пользователю деньги"
    )
    async def transfer(self, ctx, member: discord.Member = None, amount: int = None):

        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_economy"]  # Подключаемся к нужной колекции в нужной бд

        bal_a = cursor.find_one(
            {
                "guild": f"{ctx.guild.id}",
                "m_id": f"{ctx.author.id}"
            }
        )

        bal_m = cursor.find_one(
            {
                "guild": f"{ctx.guild.id}",
                "m_id": f"{member.id}"
            }
        )

        if not bal_m:
            return await ctx.send(f"{ctx.author.mention}, я не обнаружила данного юзера в базе данных.")

        balance_author = bal_a['money']


        if member.id == 706600733931339806:
            return await ctx.send(f"Я ценю то, что вы пытаетесь мне дать денег, но простите, для безопасности системы я не могу принять их.")

        if member is None:
            await ctx.send(f"{ctx.author.mention}, укажите юзера")

        if member.id == ctx.author.id:
            await ctx.send(f"{ctx.author.mention}, вы не можете первести деньги самому себе")

        else:
            if balance_author < amount:
                return await ctx.send(f"{ctx.author.mention}, у вас недостаточно кредитов для перевода")

            if amount is None:
                await ctx.send(f"{ctx.author.mention}, укажите сумму которую хотите перевести юзеру")

            if amount < 1:
                await ctx.send(f"{ctx.author.mention}, сумма не может быть ниже `1` кредита")

            else:
                mount_a = bal_a["money"] - amount
                mount_m = bal_m["money"] + amount
                if cursor.find_one({"guild": f"{ctx.guild.id}", "m_id": f"{ctx.author.id}"}):
                    cursor.update_one({"m_id": f"{ctx.author.id}"}, {'$set': {"money": mount_a}})

                if cursor.find_one({"guild": f"{ctx.guild.id}", "m_id": f"{member.id}"}):
                    cursor.update_one({"m_id": f"{member.id}"}, {'$set': {"money": mount_m}})

                emb = discord.Embed(
                    description=f"{ctx.author.mention} перевел на счет юзера {member.mention} {amount} кредит(ов)!",
                    color=config.color
                )

                await ctx.send(embed=emb)

    @commands.command(
        aliases=[
            "Лидеры",
            "лидеры"
        ],
        description="Рейтинг самых богатых пользователей сервера"
    )
    async def top(self, ctx):

        # Конект БД
        conn = pymongo.MongoClient(config.MONGODB)
        db = conn[f"RB_DB"]  # Подключаемся к нужно БД
        cursor = db[f"members_economy"]  # Подключаемся к нужной колекции в нужной бд
        limit = 11
        index = 0
        a = []

        for i in cursor.find(
                {
                    "guild": f"{ctx.guild.id}"
                }
        ).sort("money", -1):

            index += 1
            if index == limit:
                break

            if i['money'] < 1:
                break

            a.append(f"**Имя юзера** - {i['m_name']}\n**Баланс** - {i['money']}\n\n")

        embed = discord.Embed(
            title=f"Лидеры по балансу на сервере {ctx.guild.name}",
            description="".join(a),
            color=config.color
        )

        embed.set_footer(
            text='Rinuku Bot | Все права были зашифрованны в двоичный код',
            icon_url=self.bot.user.avatar_url
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(economy(client))
