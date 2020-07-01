from flask import Flask
from discord.ext import commands
import config
import threading

class RinokuBackend(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.app = Flask(__name__)

    

    @self.app.route("/")
    def main():
      return "test"


    thread1 = threading.Thread(target= self.app.run)
    thread1.start()
