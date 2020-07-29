/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const getMember = require('../utils/getMember.js');
const db = require('../utils/database.js');
const config = require('../config.json');

const randStr = () => Math.random().toString(16).slice(2);

module.exports = {
	name: 'warn',
	async execute(message, args, client) {
		if (!args[0]) {
			return await (message.reply('укажите участника!'));
		}
		const userId = getMember(args[0]);
		if (!userId) {
			return await (message.reply('Укажите участника!'));
		}

		const user = message.guild.members.cache.get(userId);

		if (!user) {
			return await (message.reply('Укажите участника!'));
		}

		const reason = args.slice(1).join(' ');

		if (!reason) {
			return await (message.reply('Укажите причину'));
		}

		const warns = await db.get(`${message.guild.id}_${user.user.id}`, 'warns', []);
		warns.push({
			moderator: message.author.id,
			reason,
			id: randStr(),
			date: new Date(),
		});


		return db.set(`${message.guild.id}_${user.user.id}`, 'warns', warns)
			.then(() => message.react('✅'))
			.then(() =>
				client.emit('nicory_warn', {
					moderator: message.author.id,
					reason,
					id: randStr(),
					date: new Date(),
					user,
				}),
			);
	},

	module: 'Модерация',
	description: 'Выдать предупреждение участнику',
	usage: 'warn <участник> <причина>',
	aliases: ['пред', 'варн'],
	permissions: ['KICK_MEMBERS'],
};
