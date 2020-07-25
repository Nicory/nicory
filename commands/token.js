/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const db = require("../utils/database.js");

const r = () => Math.random().toString(16).split(".")[1];

module.exports = {
  name: "token",
  execute(message, args, client) {
    const token = r();
    await(db.set(token, "token", message.guild.id));
    return message.author
      .send(
        `Ваш токен доступа для вебпанели(https://nicory.xyz/dashboard) сервера \`${message.guild.name}\`: ||${token}||`
      )
      .then(() =>
        message.reply(
          "ваш токен был отправлен в ЛС!\nВсе предыдущие токены этого сервера были сброшены"
        )
      )
      .catch(() =>
        message.reply(
          "у вас закрыты личные сообщения, невозможно отправить токен!"
        )
      );
  },

  module: "Утилиты",
  description: "Получить токен доступа к панели управления",
  usage: "token",
  aliases: ["токен", "control"],
  permissions: ["ADMINISTRATOR"],
};
