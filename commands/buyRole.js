const db = require('../utils/database.js');
const config = require('../config.json');
const getRole = require('../utils/getRole');

module.exports = {
	name: 'buy',
	async execute(message, args, client) {
		const roles = await (db.get(`${message.guild.id}`, 'shop', []));
		const roleId = getRole(args[0]);

		if (!args[0] || !roleId) {
			return await message.reply(`укажите роль!\nЧтоб просмотреть магазин ролей пропишите: \`shop\``);
		}

		const apiRole = message.guild.roles.cache.get(roleId);

		if (roles.filter((el) => el.id === roleId).length === 0 || !apiRole) {
			return await message.reply(`эта роль не найдена!\nЧтоб просмотреть магазин ролей пропишите: \`shop\``);
		}

		const role = roles.filter((el) => el.id == roleId)[0];
		const oldBalance = await db.get(`${message.guild.id}_${message.author.id}`, 'money', 0);
		const newBalance = oldBalance - role.price;

		await message.member.roles.add(apiRole);
		db.set(`${message.guild.id}_${message.author.id}`, 'money', newBalance).then(() => message.react('✅'));

	},
	module: 'Экономика',
	description: 'купить роль в магазине',
	usage: 'buyrole @пинг_роли',
	aliases: ['купить'],
};
