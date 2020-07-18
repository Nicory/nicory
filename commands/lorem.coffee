Discord = require "discord.js"
fetch = require "node-fetch"

module.exports = 
  name: "lorem"
  execute: (message, args, client) ->  
    sentences = args[0] || 4

    resp = await fetch("https://fish-text.ru/get?type=sentence&number=#{sentences}")
    text = await resp.json()

    if text.text.length > 1024
      return message.reply "слишком много символов в тексте!"

    embed = new Discord.MessageEmbed()
      .setDescription text.text
      .setFooter "Powered by: https://fish-text.ru/"
      .setColor 0xe155ff

    message.channel.send embed
  module: "Утилиты"
  description: "Получить текст рыбу"
  usage: "lorem [число предложений]"
  aliases: ["lipsum", "fish", "рыба"]