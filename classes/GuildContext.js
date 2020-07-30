const Discord = require("discord.js");
const GuildMemberContext = require("./GuildMemberContext");

/**
 * @class
 * @classdesc Базовый контекст вызова для гильдии
 */
class GuildContext {
  /**
   * @param {Discord.Guild} guild - участник для создания контекста
   */
  constructor(guild) {
    this.guild = guild;
  }
  /**
   * Получение контекста
   * 
   * @async
   * @returns {Promise<Object<string, any>>}
   */
  async getContext() {
    return {     
      id: this.guild.id,
      name: this.guild.name,
      icon: this.guild.iconURL(),
      region: this.guild.region,
      memberCount: this.guild.memberCount,
      createdAt: this.guild.createdAt,
      owner: await (new GuildMemberContext(this.guild.owner)).getContext()
    }
  }
}


module.exports = GuildContext;