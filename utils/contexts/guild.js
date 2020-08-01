const Discord = require("discord.js");
const role = require("./role");
const member = require("./member");

/**
 * Получение контекста для гильдии
 * @param {Discord.Guild} guild - гильдия для получения контекста
 */
module.exports = async guild => { 
  const roles = [];
  for (const role1 of guild.roles.cache) {
    roles.push(await role(role1));
  }
  
  return {
    id: guild.id,
    name: guild.name,
    icon: guild.iconURL(),
    region: guild.region,
    memberCount: guild.memberCount,
    createdAt: guild.createdAt,
    owner: await member(guild.owner),
    roles,
  };
};