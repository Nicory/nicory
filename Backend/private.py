import json
from flask import make_response
import config
from pymongo import MongoClient


def initRoutes(bot, app):
  @app.route("/private/auth/<token>", endpoint="auth")
  def auth(token):
    conn = MongoClient(config.MONGODB)
    db = conn["RB_DB"]
    cursor = db['admin_tokens']

    result = cursor.find_one({'token': token})
    if result is None:
      resp = make_response({
        'error_code': 0
      }, 401)
      return resp

    guild = bot.get_guild(result['guild'])
    if guild is None:
      return make_response({
        'error_code': 1
      }, 401)
    
    member = guild.get_member(result['member'])
    if member is None or not member.guild_permissions.administrator:
      return make_response({
          'error_code': 2
      }, 401)

    print(type(str(result['guild'])))
    return make_response({
      guild: int(result['guild']),
      member: int(result['member'])
    }, 200)

    

    

    
    
