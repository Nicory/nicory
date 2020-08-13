const db = require("../utils/database.js");

module.exports = {
  name: "bet",
  hidden: false,
  module: "Экономика",
  description: "Сделать ставку",
  aliases: ["ставка", "казино"],
  usage: "bet <сумма>",
  cooldown: 1,
  args: false,
  async execute(message, args) {
    if (!args[0]) {
      return await message.reply("укажите свою ставку!");
    }

    const balance = await db.get(`${message.guild.id}_${message.author.id}`, "money", 0);
    const amount = parseInt(args[0]);
    if (!amount) {
      return message.reply("укажите число, а не строку!(Или укажите сумму больше чем 0)");
    }
    else if (amount < 0) {
      return message.reply("число не может быть меньше 1!");
    }

    if (amount > balance) {
      return message.reply("у вас недостаточно средств для этого!");
    }

    const rand = Math.floor(Math.random() * 2);
    const moneyProcent = amount * 1.5;
    if (rand == 0) {
      message.reply(`вы проиграли ${moneyProcent}`);
      await db.set(`${message.guild.id}_${message.author.id}`, "money", balance - moneyProcent);
    }
    else if (rand == 1) {
      message.reply(`вы выиграли ${moneyProcent}`);
      await db.set(`${message.guild.id}_${message.author.id}`, "money", moneyProcent + balance);
    }
  },
};
