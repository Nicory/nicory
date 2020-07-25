module.exports = {
	name: 'steal',
	hidden: false,
	module: 'Экономика',
	description: 'Украсть деньги у юзера с шансом 50%',
	aliases: ['Украсть', 'украсть', 'Steal'],
	usage: 'steal @пинг_юзера',
	cooldown: 0,
	args: false,
	async execute(message, args, client) {
		const Discord = require('discord.js');
		const db = require('../utils/database.js');

		const getMember = require('../utils/getMember.js');
		const id = getMember(args[0]);

		const user = message.guild.members.resolve(id);
		const authorBalance = await db.get(
			`${message.guild.id}_${message.author.id}`,
			'money',
			parseInt(0),
		);
		const memberBalance = await db.get(
			`${message.guild.id}_${user.id}`,
			'money',
			parseInt(0),
		);

		const rand = Math.floor(Math.random() * 2);

		const rand2 = Math.floor(Math.random() * memberBalance);

		const proeb = (authorBalance / 100) * 50;

		if (memberBalance == parseInt(0)) {
			return message.reply('у данного юзера нету денег!');
		}

		if (user.id === message.author.id) {
			return message.reply('ты не можешь украсть деньги у самого себя!');
		}

		if (rand == 0) {
			message.reply(`вы украли у юзера ${user} ${rand2} кредитов!`);

			// Баланс мембера
			const stealedBalance = memberBalance - rand2;
			await db.set(`${message.guild.id}_${user.id}`, 'money', stealedBalance);

			// Баланс автора
			const newBalance = authorBalance + rand2;
			await db.set(
				`${message.guild.id}_${message.author.id}`,
				'money',
				newBalance,
			);
		}
		else if (rand == 1) {
			if (proeb == 0) {
				return message.reply(
					'вас заметили и вызвали полицию, вы были задержаны!',
				);
			}

			// Баланс автора
			const newBalance = authorBalance - proeb;
			await db.set(
				`${message.guild.id}_${message.author.id}`,
				'money',
				newBalance,
			);

			message.reply(
				`вас заметили и вызвали полицию, с вашего счета было снято ${proeb} кредитов!`,
			);
		}
	},
};
