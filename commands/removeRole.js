const db = require('../utils/database');

module.exports = {
	name: 'remove-role',
	hidden: false,
	module: 'Экономика',
	description: 'Удалить роль из магазина',
	aliases: ['remrole', 'удалить-роль'],
	usage:
    'remrole @пинг_роли',
	cooldown: 2,
	args: false,
	async execute(message, args, client) {
		const getRole = require('../utils/getRole');

		if (args[0] == undefined) {
			return await message.reply('укажите роль!');
		}

		const roles = await db.get(`${message.guild.id}`, 'shop', []);

		const roleId = getRole(args[0]);
		const role = message.guild.roles.cache.get(roleId);

		if (!roleId || !role) {
			return await message.reply('роль не найдена!');
		}

		if (roles.filter((el) => el.id == roleId).length == 0) {
			return message.reply('такой роли нет в магазине!');
		}
		await db.set(`${message.guild.id}`, 'shop', roles.filter((el) => el.id != roleId));
		message.react('✅');
	},
	permissions: ['ADMINISTRATOR'],
};