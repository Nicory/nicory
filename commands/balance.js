module.exports = {
    name: "balance",
    hidden: false,
    module: "Экономика",
    description: "Покажет баланс юзера",
    aliases: ['bal', 'Bal', 'Бал', 'бал', 'Баланс', 'баланс', 'balance' ],
    usage: "balance",
    cooldown: 0,
    args: false,
    async execute(message, args, client){
      const Discord = require('discord.js')
      const db = require('../utils/database.coffee')

      const getMember = require("../utils/getMember.js");
      if (args[0]==undefined) {
          var id=message.author.id
      } else {
          var id=getMember(args[0])
      }

      const user = message.guild.members.resolve(id)

      if (user.Nickname==null) {
          var nickname=user.displayName
      } else {
          var nickname=user.Nickname
      }

      let balance = await db.get(`${message.guild.id}_${message.author.id}`, 'money', 0);
      const embed = new Discord.MessageEmbed()
        .setTitle(`Баланс ${nickname}`)
        .setDescription(`${balance} <:credit:726813969167155320>`)
        .setColor('#e155ff')
        .setThumbnail(user.user.avatarURL())
      message.channel.send(embed)
    },
  };