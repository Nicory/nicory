import time
import config
import pymongo
import discord
import asyncio
from colorama import Style, Fore


class Loop:
    def __init__(self, client):
        self.bot = client

    async def mute_loop(self):
        while True:
            try:
                conn = pymongo.MongoClient(config.MONGODB)
                cursor = conn[f"RB_DB"]

                for mem in cursor[f"members_mute"].find({"mute": {"$gt": 0, "$lt": int(time.time())}}).sort([("mute", -1)]):
                    mute = mem["mute"]
                    guild = self.bot.get_guild(int(mem["guild"]))
                    if guild:
                        member = guild.get_member(int(mem["id"]))
                        if float(mute) <= float(time.time()):
                            if member and guild:
                                cursor[f"members_mute"].update({"guild": f"{guild.id}", "id": f"{member.id}"}, {'$set': {"mute": mute}})
                                mute_role = discord.utils.get(guild.roles, name="RB_Muted")
                                await member.remove_roles(mute_role, reason="Снят Мьют Временем", atomic=True)

                await asyncio.sleep(5)

            except Exception as e:
                print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"В цикле MUTE_LOOP произошла следующая ошибка:")
                print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"\n{e}")
                print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"Цикл MUTE_LOOP продолжает свою работу!")

    async def activator(self):
        loop = asyncio.get_event_loop()

        asyncio.ensure_future(self.mute_loop())

        loop.run_forever()
