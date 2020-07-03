from flask import Flask, Response
from discord.ext import commands
import config
import threading
import json

class RinokuBackend(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.app = Flask(__name__)

    

    @self.app.route("/public/fetch_commands")
    def main():
      result = []

      for command in self.bot.commands:
        if command.hidden:
          continue
        result.append({
          'name': command.name,
          'description': command.description
        })

      resp = Response(json.dumps({
        "commands": result
      }))

      resp.headers['content-type'] = "text/plain; charset=utf-8"

      return resp


    thread1 = threading.Thread(target= self.app.run)
    thread1.start()
