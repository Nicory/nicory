module.exports = {
	name: 'setlog',
	hidden: false,
	module: 'Модерация',
	description: 'Установит канал логов',
	aliases: ['logs', 'логи'],
	usage: 'setlog #пинг_канала',
	cooldown: 0,
	args: false,
	async execute(message, args, client) {
		const Discord = require('discord.js');
		const db = require('../utils/database.js');
		const getChannel = require('../utils/getChannel.js');

		const channel = getChannel(args[0].slice(2, -1));
		message.reply(channel);
		await db.get(
			`${message.guild.id}`,
			'logChannel',
		);

		await db.set(`${message.guild.id}`, 'logChannel', channel);
		message.react('✅');
	},
	permissions: ['ADMINISTRATOR'],
};
