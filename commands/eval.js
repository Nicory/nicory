const removeCodeBlock = require('../utils/removeCodeBlock');
const Discord = require('discord.js');
const util = require('util');
const haste = require('hastebin-gen');

module.exports = {
	name: 'eval',
	async execute(message, args, client) {
		if (['419524085736013834', '622747295435456512'].includes(message.author.id)) {
			const embed = new Discord.MessageEmbed();
			let success = true;
			let result = '';
			let error, start, end;
			try {
				start = new Date();
				result = util.inspect(await eval(`(async () => {${removeCodeBlock(args.join(' '))}})();`));
				end = new Date();
			}
			catch (e) {
				success = false;
				error = e;
				end = new Date();
			}
			if (result.length > 1000) {
				result = await haste(result);
			}
			if (success) {
				embed.setColor([0, 255, 0])
					.setTitle('Успех!')
					.addField(':outbox_tray: Вывод:', `\`\`\`js\n${result || '"нет вывода"'}\n\`\`\``)
					.addField(':question: Тип:', '```js\n' + typeof result + '```');
			}
			else {
				embed.setColor([255, 0, 0])
					.setTitle('Ошибка!')
					.addField(':x: Ошибка:', '```js\n' + error + '```');
			}
			embed.setFooter(`Готово за: ${end - start}ms`);
			message.channel.send(embed);
		}
	},

	hidden: true,
	usage: 'eval <code>',
	aliases: ['js'],
};
