from pymongo import MongoClient
import config
from functools import wraps



def auth(token, bot):
  conn = MongoClient(config.MONGODB)
  db = conn["RB_DB"]
  cursor = db['admin_tokens']

  result = cursor.find_one({'token': token})
  if result is None:
    return {
        'error_code': 0
    }

  guild = bot.get_guild(result['guild'])
  if guild is None:
    return {
        'error_code': 1
    }

  member = guild.get_member(result['member'])
  if member is None or not member.guild_permissions.administrator:
    return {
        'error_code': 2
    }

  return {
      'guild': int(result['guild']),
      'member': int(result['member'])
  }