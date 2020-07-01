from flask import Flask
from discord.ext import commands
import config

class RinokuBackend(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.app = Flask(__name__)

    

    @self.app.route("/")
    def main():
      return "test"

    self.app.run(port=config.api_port)
