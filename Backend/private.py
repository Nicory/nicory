import json
from flask import make_response, request, Response
import config
from pymongo import MongoClient
from Backend.utils import auth
from discord import Status
from flask_api import status as http_status

def initRoutes(bot, app):
  @app.route("/private/auth/<token>", endpoint="auth")
  def auth_token(token):
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

    return make_response({
      'guild': int(result['guild']),
      'member': int(result['member'])
    }, 200)

  @app.route("/private/info")
  def guild_info():
    if not 'Authorization' in request.headers:
      return Response(status=401)
    
    token = auth(request.headers["Authorization"], bot)
    if 'error_code' in token:
      return Response(status=401)

    gld = bot.get_guild(token['guild'])

    def fil(el):
      return el.status != Status.offline

    return {
      'name': str(gld),
      'total_members': len(gld.members),
      'online_members': len(list(filter(fil, gld.members))),
      'icon': str(gld.icon_url)
    }

    

    
    
