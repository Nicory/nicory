/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const getMember = require('../utils/getMember.js');
const db = require('../utils/database.js');
const Discord = require('discord.js');

module.exports = {
	name: 'remwarn',
	async execute(message, args, client) {
		let memberId = '';
		if (args[0]) {
			memberId = getMember(args[0]);
		}
		else {
			memberId = message.author.id;
		}

		if (!memberId) {
			return message.channel.send('Укажите участника!');
		}

		if (!args[1]) {
			return message.channel.send('Укажите ID варна!');
		}

		const member = message.guild.members.cache.get(memberId);

		const warns = await db.get(`${message.guild.id}_${member.user.id}`, 'warns', []);

		const check = warns.filter((el) => el.id === args[1]);

		if (check.length === 0) {
			return message.channel.send('Неправильный айди варна!');
		}

		const final = warns.filter((el) => el.id !== args[1]);

		return db
			.set(`${message.guild.id}_${member.user.id}`, 'warns', final)
			.then(() => message.react('✅'))
			.then(() => client.emit('nicory_unwarn', { id: args[0], moderator: message.member, member }));
	},

	module: 'Модерация',
	description: 'Снять предупреждение',
	usage: 'remwarn <участник> <айди варна>',
	aliases: ['снятьварн', 'снятьпред'],
	permissions: ['KICK_MEMBERS'],
};
