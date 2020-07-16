htmlToImage = require "node-html-to-image"


module.exports = 
  name: "html"
  execute: (message, args, client) ->  
    code = args.join(" ").replace(/{ url: '|' }/g, "");
    buffer = await htmlToImage({html: code, transparent: true})
    message.channel.send({files: [buffer]})
  module: "Утилиты"
  description: "Отрисовать HTML"
  usage: "html <код>"
  aliases: ["хтмл", "веб"]
  cooldown: 5