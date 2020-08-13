const getRole = require("../utils/getRole.js");
const db = require("../utils/database.js");

module.exports = {
  name: "modrole",
  execute(message, args) {
    return db
      .set(message.guild.id, "modRole", getRole(args[0]) || "")
      .then(() => message.react("✅"));
  },
  module: "Модерация",
  description:
    "Установка роли управляющего\nЕсли не указана роль, то мод-роль будет отключена",
  usage: "modrole [роль]",
  aliases: ["mod-role", "мод-роль", "модроль"],
  permissions: ["ADMINISTRATOR"],
};
