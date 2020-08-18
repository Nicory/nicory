const db = require("../utils/database.js");

module.exports = {
  name: "transfer",
  hidden: false,
  module: "Экономика",
  description: "передать деньги юзеру",
  aliases: ["передать"],
  usage: "transfer @пинг-юзера <количество денег>",
  cooldown: 5,
  args: false,
  async execute(message, args) {
    // Проверки
    const amount = parseInt(args.slice(1));
    if (!amount) {
      return message.reply("укажите число, а не строку!");
    }
    else if (amount < 0) {
      return message.reply("число не может быть меньше 1!");
    }

    // Получение юзера, автора и число денег
    const getMember = require("../utils/getMember.js");
    const id = getMember(args[0]);

    const author = message.author;
    const user = message.guild.members.resolve(id);

    const authorBalance = await db.get(
      `${message.guild.id}_${author.id}`,
      "money",
      parseInt(0),
    );
    const userBalance = await db.get(
      `${message.guild.id}_${user.id}`,
      "money",
      parseInt(0),
    );
    const newUserBalance = parseInt(amount + userBalance);
    const newAuthorBalance = parseInt(authorBalance - amount);

    message.reply(`передал ${user} ${amount} кредитов!`);
    await db.set(`${message.guild.id}_${user.id}`, "money", newUserBalance);
    await db.set(`${message.guild.id}_${author.id}`, "money", newAuthorBalance);
  },
};
