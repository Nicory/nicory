const Discord = require('discord.js');
/**
 * Получение контекста для канала
 * @param {Discord.TextChannel} channel- канал для получения контекста
 */
module.exports = async channel => {
	return {
		id: channel.id,
		name: channel.name,
		mention: channel.toString(),
		topic: channel.topic,
		position: channel.position,
		createdAt: channel.createdAt,
		parent: channel.parent.name,
	};
};