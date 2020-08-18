const Discord = require("discord.js");
const db = require("../utils/database.js");
const lvlUtils = require("../utils/levelsUtils.js");

module.exports = {
  name: "leaders",
  execute: async (message) => {
    const embed = new Discord.MessageEmbed()
      .setTitle(`Рейтинг участников сервера ${message.guild.name}`)
      .setDescription(
        "Этот рейтинг базируется на кол-ве опыта, которое получили участники за общение на этом сервере.\nОпыт выдается рандомно: от 10 до 25 единиц за сообщение.",
      )
      .setColor(0xe155ff)
      .setThumbnail(message.guild.iconURL());

    const exps = new Map();

    for (const i of message.guild.members.cache.array()) {
      const exp = await db.get(`${message.guild.id}_${i.user.id}`, "exp", 0);
      exps.set(i.user.id, exp);
    }

    let sorted = new Map([...exps.entries()].sort((a, b) => b[1] - a[1]));
    sorted = new Map([...sorted.entries()].slice(0, 10));

    sorted.forEach((k, v) => {
      const member = message.guild.members.cache.get(v);

      embed.addField(
        member.user.tag,
        `EXP: ${k}; LVL: ${lvlUtils.getLevelFromExp(k)}`,
      );
    });

    message.channel.send(embed);
  },
  module: "Уровни",
  description: "Топ участников сервера по уровню",
  usage: "leaders",
  aliases: ["лидеры", "топ", "top"],
};
