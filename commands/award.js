module.exports = {
  name: "award",
  hidden: false,
  module: "Экономика",
  description: "Выдаст указанное количество денег юзеру",
  aliases: ["выдать", "дать"],
  usage: "award @пинг_юзера <количество денег>",
  cooldown: 0,
  args: false,
  async execute(message, args) {
    const db = require("../utils/database.js");

    const getMember = require("../utils/getMember.js");
    const id = getMember(args[0]);

    const user = message.guild.members.resolve(id);
    const amount = parseInt(args.slice(1));
    const balance = await db.get(
      `${message.guild.id}_${user.id}`,
      "money",
      parseInt(0),
    );
    const int = parseInt(amount + balance);

    if (amount < 1) {
      return await message.reply("укажите сумму больше чем 0");
    }

    await db.set(`${message.guild.id}_${user.id}`, "money", int);
    message.reply(`Юзеру ${user} был выдано ${amount} кредитов!`);
  },
  permissions: ["ADMINISTRATOR"],
};
