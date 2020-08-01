const guild = require("./guild");
const Discord = require("discord.js");

/**
 * Получение контекста роли
 * @param {Discord.Role} role - роль для получения контекста
 */
module.exports = async role => {
  return {
    id: role.id,
    name: role.name,
    mention: role.toString(),
    position: role.position,
    managed: role.managed,
    hoisted: role.hoist,
    color: role.color,
    permissionsRaw: role.permissions?.bitfield ?? 0,
    permissions: role.permissions
  };
};