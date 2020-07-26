const db = require('../utils/database.js');
const config = require('../config.json');

module.exports = {
	name: 'buy',
	async execute(message, args, client) {
		const roles = await (db.get(`${message.guild.id}`, 'shop', []));

		if (!args[0]) {
			return await message.reply(`укажите роль!\nЧтоб просмотреть магазин ролей пропишите: \`${config.prefix}shop\``);

		}

		if (roles.filter((el) => el.name === args[0]).length === 0) {
			return await message.reply(`эта роль не найдена!\nЧтоб просмотреть магазин ролей пропишите: \`${config.prefix}shop\``);
		}
	},
	module: 'Экономика',
	description: 'купить роль в магазине',
	usage: 'buyrole @пинг_роли',
	aliases: ['купить'],
};
