from flask import Flask, Response, request
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

    @self.app.after_request
    def apply_caching(response):
      response.headers["Server"] = f"RinokuBot/{config.version}"
      return response
    

    thread1 = threading.Thread(target= self.app.run)
    thread1.start()
