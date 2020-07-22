getMember = require "../utils/getMember.js"
db = require "../utils/database.coffee"
Discord = require "discord.js"

module.exports = 
  name: "remwarn"
  execute: (message, args, client) ->  
    memberId = ""
    if args[0]
      memberId = getMember args[0]
    else
      memberId = message.author.id

    if !memberId
      return message.channel.send "Укажите участника!"

    if !args[1]
      return message.channel.send "Укажите ID варна!"

    member = message.guild.members.cache.get memberId

    warns = await db.get("#{message.guild.id}_#{member.user.id}", "warns", [])

    check = warns.filter (el) -> el.id == args[1]

    if check.length == 0
      return message.channel.send "Неправильный айди варна!"

    final = warns.filter (el) -> el.id != args[1]

    db.set("#{message.guild.id}_#{member.user.id}", "warns", final).then () ->
      message.react "✅"

    
      

  module: "Модерация"
  description: "Снять предупреждение"
  usage: "remwarn <участник> <айди варна>"
  aliases: ["снятьварн", "снятьпред"]
  permissions: ["KICK_MEMBERS"]