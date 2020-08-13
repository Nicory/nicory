const role = require("./role");
const member = require("./member");
const channel = require("./channel");

/**
 * Получение контекста для гильдии
 * @param {Discord.Guild} guild - гильдия для получения контекста
 */
module.exports = async guild => {
  const roles = [];
  for (const role1 of guild.roles.cache) {
    roles.push(await role(role1));
  }
  let channels = await guild.channels.cache.filter(g => g.type == "text").array(i => i);
  let members = await guild.members.cache.array(i => i);

  let parsedCh = [];
  let parsedMem = [];

  for(const ch of channels) {
    parsedCh.push(await channel(ch));
  }

  for(const mem of members) {
    parsedMem.push(await member(mem));
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
    channels: parsedCh,
    getTextChannel(id){
      return parsedCh.filter(i => i.id == id)[0];
    },
    getMember(id){
      return parsedMem.filter(n => n.id == id)[0];
    }
  };
};