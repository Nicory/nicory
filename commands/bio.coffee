db = require "../utils/database.coffee"

module.exports = 
  name: "bio"
  execute: (message, args, client) ->  
    if !args[0]
      return message.channel.send "Укажите текст!"
    
    db.set("#{message.guild.id}_#{message.author.id}", "bio", args.join(" ")).then () -> message.react "✅"

  module: "Утилиты"
  description: "Пинг бота до серверов Discord"
  usage: "bio <текст>"
  aliases: ["био", "осебе"]