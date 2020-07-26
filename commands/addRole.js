module.exports = {
	name: 'addrole',
	hidden: false,
	module: 'Экономика',
	description: 'Добавить роль в магазин',
	aliases: ['добавить-роль'],
	usage:
    'addrole @пинг_роли <цена>',
	cooldown: 2,
	args: false,
	async execute(message, args, client) {
		const Discord = require('discord.js');
		const db = require('../utils/database.js');

		if (args[0] == undefined) {
			return await message.reply('укажите роль!');
		}

		if (args[1] == undefined) {
			return await message.reply('укажите цену роли!');
		}


		const name = args[0].slice(3, -1);
		const price = parseInt(args[1]);

		if (!price) {
			return await message.reply('укажи число, а не строку!');
		}

		const roles = await db.get(`${message.guild.id}`, 'shop', []);
		if (roles.length >= 25) {
			return message.reply('достигнут лимит работ(25)!');
		}
		if (roles.filter((el) => el.name == name).length != 0) {
			return message.reply('такая роль уже есть в магазине!');
		}
		roles.push({ name: name, price });
		await db.set(`${message.guild.id}`, 'shop', roles);
		message.react('✅');
	},
	permissions: ['ADMINISTRATOR'],
};
