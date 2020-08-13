module.exports = {
  name: "balance",
  hidden: false,
  module: "Экономика",
  description: "Покажет баланс юзера",
  aliases: ["bal", "бал", "баланс"],
  usage: "balance",
  cooldown: 0,
  args: false,
  async execute(message, args) {
    const Discord = require("discord.js");
    const db = require("../utils/database.js");

    const getMember = require("../utils/getMember.js");

    let id, nickname;

    if (args[0] == undefined) {
      id = message.author.id;
    }
    else {
      id = getMember(args[0]);
    }

    const user = message.guild.members.resolve(id);

    if (user.nickname == null) {
      nickname = user.user.tag;
    }
    else {
      nickname = user.nickname;
    }

    const balance = await db.get(`${message.guild.id}_${user.id}`, "money", 0);
    const embed = new Discord.MessageEmbed()
      .setTitle(`Баланс ${nickname}`)
      .setDescription(`${balance} <:credit:726813969167155320>`)
      .setColor("#e155ff")
      .setThumbnail(user.user.avatarURL());
    message.channel.send(embed);
  },
};
