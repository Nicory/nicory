const guild = require("./guild");
const member = require("./member");
const channel = require("./channel");
const msg = require("./message");

/**
 * Получение контекста вызова
 * @param {Discord.Message} message - сообщение для получения контекста
 */
module.exports = async (message) => {
  return {
    channel: await channel(message.channel),
    member: await member(message.member),
    guild: await guild(message.guild),
    message: await msg(message),
  };
};
