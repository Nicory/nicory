getMember = require "../utils/getMember.js"
db = require "../utils/database.coffee"
Discord = require "discord.js"

module.exports = 
  name: "warns"
  execute: (message, args, client) ->  
    memberId = ""
    if args[0]
      memberId = getMember args[0]
    else
      memberId = message.author.id

    if !memberId
      return message.channel.send "Укажите участника!"

    member = message.guild.members.cache.get memberId

    warns = await db.get("#{message.guild.id}_#{member.user.id}", "warns", [])

    embed = new Discord.MessageEmbed()
      .setTitle("Предупреждения участника #{member.user.tag}")
      .setThumbnail(member.user.avatarURL())
      .setColor(0xe155ff)

    if warns.length == 0
      embed.setDescription "У участника нет предупреждений"
      return message.channel.send embed

    for warn in warns
      embed.addField("ID: #{warn.id}; DATE: #{new Date(warn.date).toLocaleString()}; MODER: #{message.guild.members.cache.get(warn.moderator).user.tag}", warn.reason)
    
    message.channel.send embed
      

  module: "Модерация"
  description: "Просмотреть предупреждения участника"
  usage: "warns [участник]"
  aliases: ["преды", "варны"]