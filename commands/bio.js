/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const db = require("../utils/database.js");

module.exports = {
  name: "bio",
  execute(message, args, client) {
    if (!args[0]) {
      return message.channel.send("Укажите текст!");
    }

    return db
      .set(`${message.guild.id}_${message.author.id}`, "bio", args.join(" "))
      .then(() => message.react("✅"));
  },

  module: "Утилиты",
  description: "Информация о себе",
  usage: "bio <текст>",
  aliases: ["био", "осебе"],
};
