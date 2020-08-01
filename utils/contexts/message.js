const Discord = require("discord.js");
const role = require("./role");
const member = require("./member");
const channel = require("./channel");
const guild = require("./guild");

/**
 * Получение контекста для сообщения
 * @param {Discord.Message} message - сообщение для получения контекста
 */
module.exports = async message => { 
  const memberMentions = [];
  for (const mention of message.mentions.members.array((e) => e)) {
    if (typeof mention == "string") continue;
    memberMentions.push(await member(mention));
  }
  const channelMentions = [];
  for (const mention of message.mentions.channels.array((e) => e)) {
    if (typeof mention == "string") continue;
    channelMentions.push(await channel(mention));
  }
  const roleMentions = [];
  for (const mention of message.mentions.roles.array((e) => e)) {
    if (typeof mention == "string") continue;
    roleMentions.push(await role(mention));
  }
  return {
    author: await member(message.member),
    id: message.id,
    content: message.content,
    guild: await guild(message.guild),
    createdAt: message.createdAt,
    url: message.url,
    mentions: {
      members: memberMentions,
      channels: channelMentions,
      roles: roleMentions,
    },
    channel: await channel(message.channel),
  };
};