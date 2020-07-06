from flask import Flask, Response
from discord.ext import commands
import config
import threading
import json
from Backend.public import initRoutes
from Backend.private import initRoutes as privateInitRoutes

class RinokuBackend(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.app = Flask(__name__)

    initRoutes(self.bot, self.app)
    privateInitRoutes(self.bot, self.app)
    

    thread1 = threading.Thread(target= self.app.run)
    thread1.start()
