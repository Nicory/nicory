module.exports = {
	name: 'shop',
	hidden: false,
	module: 'Экономика',
	description: 'Покажет магазин сервера',
	aliases: [ 'магаз', 'магазин' ],
	usage: 'shop',
	cooldown: 2,
	args: false,
	async execute(message, args, client) {
		const Discord = require('discord.js');
		const db = require('../utils/database.js');
		const getRol = require('../utils/getRole');

		const roles = await (db.get(message.guild.id, 'shop', []));
		const embed = new Discord.MessageEmbed()
			.setColor(0xe155ff)
			.setThumbnail(message.guild.iconURL())
			.setTitle(`Магазин сервера ${message.guild.name}`)
			.setDescription('Роль можно купить с помощью команды `buy <id или @упоминание>`');
		if (roles.length === 0) {
			embed.setDescription(
				'Магазин пуст!',
			);
			return await (message.channel.send(embed));
		}

		for (const role of Array.from(roles)) {
			const apiRole = message.guild.roles.cache.get(role.id).name;
			embed.addField(`${apiRole} (${role.id})`, `Цена: ${role.price}`);
		}

		return message.channel.send(embed);
	},

};