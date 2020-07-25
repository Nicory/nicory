/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const getMember = require('../utils/getMember');

module.exports = {
	name: 'ban',
	execute(message, args, client, usage) {
		const userId = getMember(args[0]);

		if (!userId) {
			return usage();
		}

		const member = message.guild.members.cache.get(userId);

		if (!member) {
			return usage();
		}

		if (member.roles.highest.position >= message.member.roles.highest.position) {
			return message.reply('вы не можете кикнуть этого участника!');
		}

		let reason = args.slice(1).join(' ');

		if (!reason) {
			reason = 'не указано';
		}


		member.user.send(`Вы были забанены на сервере ${message.guild.name} по причине \`${reason}\``);
		message.react('✅');
		return member.ban({ reason });
	},


	module: 'Модерация',
	description: 'Забанить пользователя',
	usage: 'ban <юзер> [причина]',
	aliases: ['бан'],
	permissions: ['BAN_MEMBERS'],
};