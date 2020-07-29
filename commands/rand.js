module.exports = {
	name: 'random',
	hidden: false,
	module: 'Веселости',
	description: 'Выберет рандомное число',
	aliases: ['ранд', 'рандом' ],
	usage: 'ранд <число>',
	cooldown: 0,
	args: false,
	async execute(message, args, client) {
		const Discord = require('discord.js');
		if (args[0] == undefined) {
			return await message.reply('укажите цифру!');
		}

		const num = args;
		if (num > 10000) {
			return await message.reply('Я не могу обрабатывать настолько большие числа!');
		}
		const answer = Math.floor(Math.random() * num);
		await message.reply(answer);

	},
};