module.exports = {
  name: "addjob",
  hidden: false,
  module: "Экономика",
  description: "Покажет магазин сервера",
  aliases: [ 'добавить-роль', 'добавить-в-магазин' ],
  usage: "addjob @пинг_роль <минимальная зарплата <максимальная зарплата>",
  cooldown: 2,
  args: false,
  async execute(message, args, client){
    const Discord = require('discord.js')
    const db = require('../utils/database.coffee')

    if (args[0]==undefined) {
      return await message.reply('укажите имя работы!')
    }

    if (args[1]==undefined) {
      return await message.reply('укажите мин. зарплату на этой работе!')
    }

    if (args[2] == undefined) {
      return await message.reply('укажите макс. зарплату на этой работе!')
    }

    let name = args[0];
    let min = parseInt(args[1]);
    let max = parseInt(args[2]);


    let job = await db.get(`${message.guild.id}`, 'customJobs', []);
    if (job.filter(el => el.name == name).length != 0) { 
      return message.reply("такая работа уже существует!");
    }
    job.push({name: name, min, max});
    await db.set(`${message.guild.id}`, 'customJobs', job);
    message.react("✅")
  },
  permissions: ["ADMINISTRATOR"]
};