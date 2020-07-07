import json
from flask import Response

def initRoutes(bot, app):
  @app.route("/public/fetch_commands", endpoint="fetch_commands", methods=["GET"])
  def fetch_commands():
      result = []

      for command in bot.commands:
          if command.hidden:
            continue
          result.append({
              'name': command.name,
              'description': command.description
          })

      resp = Response(json.dumps({"commands": result}))

      resp.headers['content-type'] = "text/plain; charset=utf-8"

      return resp
