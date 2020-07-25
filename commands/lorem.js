/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const Discord = require("discord.js");
const fetch = require("node-fetch");

module.exports = { 
  name: "lorem",
  execute(message, args, client) {  
    const sentences = args[0] || 4;

    const resp = await(fetch(`https://fish-text.ru/get?type=sentence&number=${sentences}`));
    const text = await(resp.json());

    if (text.text.length > 1024) {
      return message.reply("слишком много символов в тексте!");
    }

    const embed = new Discord.MessageEmbed()
      .setDescription(text.text)
      .setFooter("Powered by: https://fish-text.ru/")
      .setColor(0xe155ff);

    return message.channel.send(embed);
  },
  module: "Утилиты",
  description: "Получить текст рыбу",
  usage: "lorem [число предложений]",
  aliases: ["lipsum", "fish", "рыба"]
};