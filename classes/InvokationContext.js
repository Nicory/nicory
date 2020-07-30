const Discord = require("discord.js");
const GuildMemberContext = require("./GuildMemberContext");
const BaseContext = require("./BaseContext");

/**
 * @class
 * @classdesc Базовый контекст вызова для кастом команд
 * @implements {BaseContext}
 */
class InvokationContext extends BaseContext { 
  /**
   * @param {Discord.Message} message - сообщение для создания контекста
   */
  constructor(message) { 
    this.message = message;
  }
  /**
   * Получение контекста
   * 
   * @async
   * @returns {Promise<Object<string, any>>}
   */
  async getContext() { 
    return {
      guild: await (new GuildContext(this.message.guild)).getContext(),
      member: await (new GuildMemberContext(this.message.member)).getContext()
    }
  }
}

module.exports = InvokationContext;