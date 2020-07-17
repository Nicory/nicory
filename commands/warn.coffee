getMember = require "../utils/getMember.js"
mongodb = require "mongodb"
config = require "../config.json"

randStr = () -> Math.random().toString(16).slice 2

module.exports = 
  name: "warn"
  execute: (message, args, client, sendUsage) ->  
    if !args[0]
      await message.reply "укажите участника!"
    userId = getMember args[0]
    if !userId
      await message.reply "Укажите участника!"

    user = message.guild.members.cache.get userId

    if !user
      await message.reply "Укажите участника!"
    
    reason = args.slice(1).join " "

    if !reason
      await message.reply "Укажите причину"

    connection = await mongodb.MongoClient.connect config.mongo
    col = connection.db("nicory").collection "warns"

    col.insertOne({guild: message.guild.id, member: user.user.id, moderator: message.author.id, reason: reason, id: randStr()}).then () -> 
      message.react "✅"




  module: "Модерация"
  description: "Выдать предупреждение участнику"
  usage: "warn <участник> <причина>"
  aliases: ["пред", "варн"]
  permissions: ["KICK_MEMBERS"]