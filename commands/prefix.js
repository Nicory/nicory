const db = require('../utils/database');
const config = require("../config.json");

module.exports = {
  name: 'prefix',
  async execute(message, args, client) {
    if (!args[0]) {
      message.channel.send(`Префикс на этом сервере: \`${await db.get(message.guild.id, 'prefix', config.prefix)}\``);
    } else {
      if (args[0].match(/(\s|`)/) || args[0].length > 10) {
        return message.channel.send('Некорректный префикс!');
      } else { 
        await db.set(message.guild.id, 'prefix', args[0]);
        message.react('✅')
      }
    }
  },
  module: 'Утилиты',
  description: 'Смена префикса',
  usage: 'prefix <префикс>',
  aliases: ['префикс'],
  permissions: ["ADMINISTRATOR"]
};