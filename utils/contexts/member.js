const db = require("../database");
const role = require("./role");

/**
 * Получение контекста участника
 * @param {Discord.GuildMember} member - участник для получения контекста
 */
module.exports = async member => {
  const roles = [];
  for (const role2 of roles) {
    roles.push(await role(role2));
  }

  return {
    id: member.user.id,
    mention: member.toString(),
    nickname: member.nickname ?? member.user.username,
    tag: member.user.tag,
    bot: member.user.bot,
    name: member.user.username,
    discriminator: member.user.discriminator,
    joinedAt: member.joinedAt,
    createdAt: member.user.createdAt,
    avatar: member.user.avatarURL(),
    bio: await db.get(
      `${member.guild.id}_${member.user.id}`,
      "bio",
      "Отсутствует",
    ),
    exp: await db.get(
      `${member.guild.id}_${member.user.id}`,
      "exp",
      0,
    ),
    roles,
    hasPermission(name) {
      return member.hasPermission(name);
    },
    addRole(id){
      return member.roles.add(id);
    },
    removeRole(id){
      return member.roles.remove(id);
    },
    ban(reason = "Шаблонный движок") {
      return member.ban({reason});
    },
    kick(reason = "Шаблонный движок") {
      return member.kick(reason);
    }
  };
};