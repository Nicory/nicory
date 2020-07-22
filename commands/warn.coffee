getMember = require "../utils/getMember.js"
db = require "../utils/database.coffee"
config = require "../config.json"

randStr = () -> Math.random().toString(16).slice 2

module.exports = 
  name: "warn"
  execute: (message, args, client, sendUsage) ->  
    if !args[0]
      return await message.reply "укажите участника!"
    userId = getMember args[0]
    if !userId
      return await message.reply "Укажите участника!"

    user = message.guild.members.cache.get userId

    if !user
      return await message.reply "Укажите участника!"
    
    reason = args.slice(1).join " "

    if !reason
      return await message.reply "Укажите причину"

    console.dir user.user.id

    warns = await db.get("#{message.guild.id}_#{user.user.id}", "warns", [])
    warns.push {moderator: message.author.id, reason: reason, id: randStr(), date: new Date()}

    db.set("#{message.guild.id}_#{user.user.id}", "warns", warns).then () ->
      message.react "✅"



  module: "Модерация"
  description: "Выдать предупреждение участнику"
  usage: "warn <участник> <причина>"
  aliases: ["пред", "варн"]
  permissions: ["KICK_MEMBERS"]