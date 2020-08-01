const removeCodeBlock = require('../utils/removeCodeBlock');
const invokation = require('../utils/contexts/invokation');
const template = require('../utils/renderTemplate');
<<<<<<< HEAD
const { MessageEmbed } = require('discord.js');
=======
>>>>>>> parent of a907f07... moving to ejs

module.exports = {
	name: 'template',
	async execute(message, args, client) {
<<<<<<< HEAD
		const context = await invokation(message);
		const code = removeCodeBlock(args.join(' '));
		try {
			const output = template(code, context);
			message.channel.send(output.length == 0 ? 'Шаблон не вывел данных' : output);
		}
		catch (e) {
			const embed = new MessageEmbed()
				.setColor(0xff0000)
				.setTitle('Ошибка!')
				.setDescription('При компиляции была обнаружена следующая ошибка:\n' + `\`\`\`\n${e}\`\`\``);
			message.channel.send(embed);
		}
=======
    const context = await invokation(message);
		const code = removeCodeBlock(args.join(' '));
		message.channel.send(template(code, context));
>>>>>>> parent of a907f07... moving to ejs
	},
	module: 'Утилиты',
	description: 'Запуск шаблона сообщения',
	usage: 'template <код>',
	aliases: ['шаблон', 'hbs'],
	permissions: ['ADMINISTRATOR'],
};