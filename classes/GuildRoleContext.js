const Discord = require("discord.js");
const GuildContext = require("./GuildContext");

/**
 * @class
 * @classdesc Базовый контекст вызова для роли
 */
class GuildRoleContext {
  /**
   * @param {Discord.Role} role - роль для создания контекста
   */
  constructor(role) {
    this.role = role;
  }
  /**
   * Получение контекста
   *
   * @async
   * @returns {Promise<Object<string, any>>}
   */
  async getContext() {
    return {
      id: this.role.id,
      name: this.role.name,
      guild: await new GuildContext(this.role.guild).getContext(),
      mention: this.role.toString(),
      position: this.role.position,
      managed: this.role.managed,
      hoisted: this.role.hoist,
      color: this.role.color,
      permissionsRaw: this.role.permissions.bitfield,
      permissions: this.role.permissions
    };
  }
}

module.exports = GuildRoleContext;
