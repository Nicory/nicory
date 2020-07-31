const Discord = require("discord.js");
const GuildMemberContext = require("./GuildMemberContext");
const GuildContext = require("./GuildContext");
const MessageContext = require("./MessageContext");

/**
 * @class
 * @classdesc Базовый контекст вызова для кастом команд
 */
class InvokationContext { 
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
      member: await (new GuildMemberContext(this.message.member)).getContext(),
      message: await (new MessageContext(this.message)).getContext()
    }
  }
}

module.exports = InvokationContext;