const Discord = require('discord.js');
const role = require('./role');
const member = require('./member');
const channel = require('./channel');

/**
 * Получение контекста для гильдии
 * @param {Discord.Guild} guild - гильдия для получения контекста
 */
module.exports = async guild => {
	const roles = [];
	for (const role1 of guild.roles.cache) {
		roles.push(await role(role1));
	}
	const channels = guild.channels.cache.filter(g => g.type == "text").array(async e => await channel(e));

	return {
		id: guild.id,
		name: guild.name,
		icon: guild.iconURL(),
		region: guild.region,
		memberCount: guild.memberCount,
		createdAt: guild.createdAt,
		owner: await member(guild.owner),
		roles,
		channels,
		getTextChannel(id){
			return channels.filter(i => i.id == id)[0];
		}
	};
};