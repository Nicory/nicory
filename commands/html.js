/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const htmlToImage = require("node-html-to-image");

module.exports = { 
  name: "html",
  execute(message, args, client) { 
    message.channel.startTyping(); 
    const code = args.join(" ").replace(/{ url: '|' }/g, "");
    const buffer = await(htmlToImage({html: code, transparent: true}));
    await(message.channel.send({files: [buffer]}));
    return message.channel.stopTyping();
  },
  module: "Утилиты",
  description: "Отрисовать HTML",
  usage: "html <код>",
  aliases: ["хтмл", "веб"],
  cooldown: 5
};