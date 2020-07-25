/*
 * decaffeinate suggestions:
 * DS101: Remove unnecessary use of Array.from
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const getMember = require('../utils/getMember.js');
const db = require('../utils/database.js');
const Discord = require('discord.js');

module.exports = {
	name: 'warns',
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

		const member = message.guild.members.cache.get(memberId);

		const warns = await db.get(`${message.guild.id}_${member.user.id}`, 'warns', []);

		const embed = new Discord.MessageEmbed()
			.setTitle(`Предупреждения участника ${member.user.tag}`)
			.setThumbnail(member.user.avatarURL())
			.setColor(0xe155ff);

		if (warns.length === 0) {
			embed.setDescription('У участника нет предупреждений');
			return message.channel.send(embed);
		}

		for (const warn of Array.from(warns)) {
			embed.addField(
				`ID: ${warn.id}; DATE: ${new Date(
					warn.date,
				).toLocaleString()}; MODER: ${
					message.guild.members.cache.get(warn.moderator).user.tag
				}`,
				warn.reason,
			);
		}

		return message.channel.send(embed);
	},

	module: 'Модерация',
	description: 'Просмотреть предупреждения участника',
	usage: 'warns [участник]',
	aliases: ['преды', 'варны'],
};
