const db = require("../utils/database.js");

module.exports = {
  name: "userinfo",
  module: "Основное",
  description: "Информация про юзера",
  aliases: ["юзер", "юзеринфо", "user"],
  usage: "userinfo",
  args: false,
  async execute(message, args) {
    const Discord = require("discord.js");

    let id, nickname, status;

    const getMember = require("../utils/getMember.js");
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

    // Чек статуса
    if (user.presence.status == "online") {
      status = "<:online:728682549819473970> Онлайн";
    }
    else if (user.presence.status == "idle") {
      status = "<:idle:728682549890515094> Отошёл";
    }
    else if (user.presence.status == "dnd") {
      status = "<:dnd:728682911057838140> Не беспокоить";
    }
    else if (user.presence.status == "offline") {
      status = "<:9819_Offline:728682548280033281> Оффлайн";
    }
    else {
      status = "Произошла ошибка!";
    }

    const embed = new Discord.MessageEmbed()
      .setColor("#e155ff")
      .setTitle(`${nickname}`)
      .setAuthor("Информация про пользователя")
      .setDescription(
        await db.get(
          `${message.guild.id}_${user.user.id}`,
          "bio",
          "Пользователь не указал информацию о себе",
        ),
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
