const Discord = require('discord.js');
const GuildMemberContext = require('./GuildMemberContext');
const GuildContext = require('./GuildContext');

/**
 * @class
 * @classdesc Базовый контекст вызова для канала
 */
class GuildChannelContext {
	/**
   * @param {Discord.TextChannel} channel - канал для создания контекста
   */
	constructor(channel) {
		this.channel = channel;
	}
	/**
   * Получение контекста
   *
   * @async
   * @returns {Promise<Object<string, any>>}
   */
	async getContext() {
		return {
			id: this.channel.id,
			name: this.channel.name,
			guild: await new GuildContext(this.channel.guild).getContext(),
			mention: this.channel.toString(),
			topic: this.channel.topic,
			position: this.channel.position,
			createdAt: this.channel.createdAt,
			parent: this.channel.parent.name,
		};
	}
}

module.exports = GuildChannelContext;
