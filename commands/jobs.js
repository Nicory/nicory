/*
 * decaffeinate suggestions:
 * DS101: Remove unnecessary use of Array.from
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const db = require("../utils/database.js");
const Discord = require("discord.js");

module.exports = {
  name: "jobs",
  execute(message, args, client) {
    const jobs = await(db.get(message.guild.id, "customJobs", []));
    const embed = new Discord.MessageEmbed()
      .setColor(0xe155ff)
      .setThumbnail(message.guild.iconURL())
      .setTitle(`Работы сервера ${message.guild.name}`);
    if (jobs.length === 0) {
      embed.setDescription(
        "Работ не найдено, но вы их можете добавить с помощью команды `addjob`"
      );
      return await(message.channel.send(embed));
    }

    for (let job of Array.from(jobs)) {
      embed.addField(job.name, `${job.min}/${job.max}`);
    }

    return message.channel.send(embed);
  },

  module: "Экономика",
  description: "Список работ на сервере",
  usage: "jobs",
  aliases: ["работы"],
};
