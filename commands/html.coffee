htmlToImage = require "node-html-to-image"

module.exports = 
  name: "html"
  execute: (message, args, client) -> 
    message.channel.startTyping() 
    code = args.join(" ").replace(/{ url: '|' }/g, "");
    buffer = await htmlToImage({html: code, transparent: true})
    await message.channel.send({files: [buffer]})
    message.channel.stopTyping()
  module: "Утилиты"
  description: "Отрисовать HTML"
  usage: "html <код>"
  aliases: ["хтмл", "веб"]
  cooldown: 5