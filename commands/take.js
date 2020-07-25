module.exports = {
	name: 'take',
	hidden: false,
	module: 'Экономика',
	description: 'Заберет указанное количество денег у юзера',
	aliases: ['take', 'Забрать', 'забрать', 'Взять', 'взять'],
	usage: 'take @пинг_юзера <количество денег>',
	cooldown: 0,
	args: false,
	async execute(message, args, client) {
		const Discord = require('discord.js');
		const db = require('../utils/database.js');

		const getMember = require('../utils/getMember.js');
		const id = getMember(args[0]);

		const user = message.guild.members.resolve(id);
		const amount = parseInt(args.slice(1));
		const balance = await db.get(
			`${message.guild.id}_${user.id}`,
			'money',
			parseInt(0),
		);
		const int = parseInt(balance - amount);

		if (amount < 1) {
			return await message.reply('укажите сумму больше чем 0');
		}

		await db.set(`${message.guild.id}_${user.id}`, 'money', int);
		message.reply(`С баланса ${user} было снято ${amount} кредитов!`);
	},
	permissions: ['ADMINISTRATOR'],
};
