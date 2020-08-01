const removeCodeBlock = require('../utils/removeCodeBlock');
const invokation = require('../utils/contexts/invokation');
const template = require('../utils/renderTemplate');

module.exports = {
	name: 'template',
	async execute(message, args, client) {
    const context = await invokation(message);
		const code = removeCodeBlock(args.join(' '));
		message.channel.send(template(code, context));
	},
	module: 'Утилиты',
	description: 'Запуск шаблона сообщения',
	usage: 'template <код>',
	aliases: ['шаблон', 'hbs'],
	permissions: ['ADMINISTRATOR'],
};