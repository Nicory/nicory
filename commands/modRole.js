/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const getRole = require('../utils/getRole.js');
const db = require('../utils/database.js');

module.exports = {
	name: 'modrole',
	execute(message, args, client) {
		return db
			.set(message.guild.id, 'modRole', getRole(args[0]) || '')
			.then(() => message.react('✅'));
	},
	module: 'Модерация',
	description:
    'Установка роли управляющего\nЕсли не указана роль, то мод-роль будет отключена',
	usage: 'modrole [роль]',
	aliases: ['mod-role', 'мод-роль', 'модроль'],
	permissions: ['ADMINISTRATOR'],
};
