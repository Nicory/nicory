const Discord = require('discord.js');
const GuildMemberContext = require('./GuildMemberContext');
const GuildRoleContext = require('./GuildRoleContext');

/**
 * @class
 * @classdesc Базовый контекст вызова для гильдии
 */
class GuildContext {
	/**
   * @param {Discord.Guild} guild - гильдия для создания контекста
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
		const roles = [];
		for (const role of this.guild.roles.cache) {
			roles.push(await new GuildRoleContext(role).getContext());
		}
		return {
			id: this.guild.id,
			name: this.guild.name,
			icon: this.guild.iconURL(),
			region: this.guild.region,
			memberCount: this.guild.memberCount,
			createdAt: this.guild.createdAt,
			owner: await (new GuildMemberContext(this.guild.owner)).getContext(),
			roles,
		};
	}
}


module.exports = GuildContext;