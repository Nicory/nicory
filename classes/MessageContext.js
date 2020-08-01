const Discord = require("discord.js");
const GuildMemberContext = require("./GuildMemberContext");
const GuildContext = require("./GuildContext");
const GuildChannelContext = require("./GuildChannelContext");
const GuildRoleContext = require("./GuildRoleContext");

/**
 * @class
 * @classdesc Базовый контекст вызова для сообщения
 */
class MessageContext {
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
    const memberMentions = [];
    for (const mention of this.message.mentions.members.array(e => e)) {
      if (typeof mention == "string") continue;
      memberMentions.push(await (new GuildMemberContext(mention)).getContext());
    }
    const channelMentions = [];
    for (const mention of this.message.mentions.channels.array((e) => e)) {
      if (typeof mention == "string") continue;
      channelMentions.push(await new GuildChannelContext(mention).getContext());
    }
    const roleMentions = [];
    for (const mention of this.message.mentions.roles.array((e) => e)) {
      if (typeof mention == "string") continue;
      roleMentions.push(await new GuildRoleContext(mention).getContext());
    }
    return {
      id: this.message.id,
      content: this.message.content,
      guild: await new GuildContext(this.message.guild).getContext(),
      author: await new GuildMemberContext(this.message.member).getContext(),
      createdAt: this.message.createdAt,
      url: this.message.url,
      mentions: {
        members: memberMentions,
        channels: channelMentions,
        roles: roleMentions
      },
      channel: await new GuildChannelContext(this.message.channel).getContext(),
    };
  }
}


module.exports = MessageContext;