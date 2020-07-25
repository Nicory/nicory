const db = require("../utils/database.js");

module.exports = {
  name: "userinfo",
  module: "Основное",
  description: "Информация про юзера",
  aliases: ["юзер", "юзеринфо", "user"],
  usage: "userinfo",
  args: false,
  async execute(message, args, client) {
    const Discord = require("discord.js");
    const package = require("../package.json");
    const config = require("../config.json");

    const getMember = require("../utils/getMember.js");
    if (args[0] == undefined) {
      var id = message.author.id;
    } else {
      var id = getMember(args[0]);
    }

    const user = message.guild.members.resolve(id);

    if (user.Nickname == null) {
      var nickname = user.displayName;
    } else {
      var nickname = user.Nickname;
    }

    // Чек статуса
    if (user.presence.status == "online") {
      var status = "<:online:728682549819473970> Онлайн";
    } else if (user.presence.status == "idle") {
      var status = "<:idle:728682549890515094> Отошёл";
    } else if (user.presence.status == "dnd") {
      var status = "<:dnd:728682911057838140> Не беспокоить";
    } else if (user.presence.status == "offline") {
      var status = "<:9819_Offline:728682548280033281> Оффлайн";
    } else {
      var status = "Произошла ошибка!";
    }

    const embed = new Discord.MessageEmbed()
      .setColor("#e155ff")
      .setTitle(`${nickname}`)
      .setAuthor("Информация про пользователя")
      .setDescription(
        await db.get(
          `${message.guild.id}_${user.user.id}`,
          "bio",
          "Пользователь не указал информацию о себе"
        )
      )
      .addFields({
        name: "Основная информация:",
        value: `Имя пользователя: ${user}\nАккаунт создан: \nПрисоединился: \nСтатус: ${status}\nИграет в: ${
          user.presence.activities.length != 0
            ? user.presence.activities.join(" ")
            : "ничто"
        }`,
      })
      .setFooter(`ID: ${user.id}`)
      .setThumbnail(user.user.avatarURL());
    message.channel.send(embed);
  },
};
