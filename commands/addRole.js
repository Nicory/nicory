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
		const getRole = require('../utils/getRole');

		if (args[0] == undefined) {
			return await message.reply('укажите роль!');
		}

		if (args[1] == undefined) {
			return await message.reply('укажите цену роли!');
		}


		const roleId = getRole(args[0]);
		const role = message.guild.roles.cache.get(roleId);
		const price = parseInt(args[1]);

		if (!roleId || !role) {
			return await message.reply('роль не найдена!');
		}

		if (!price) {
			return await message.reply('укажи число, а не строку!');
		}

		const roles = await db.get(`${message.guild.id}`, 'shop', []);
		if (roles.length >= 25) {
			return message.reply('достигнут лимит ролей(25)!');
		}
		if (roles.filter((el) => el.id == roleId).length != 0) {
			return message.reply('такая роль уже есть в магазине!');
		}
		roles.push({ id: roleId, price });
		await db.set(`${message.guild.id}`, 'shop', roles);
		message.react('✅');
	},
	permissions: ['ADMINISTRATOR'],
};
