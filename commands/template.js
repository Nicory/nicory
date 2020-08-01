const removeCodeBlock = require('../utils/removeCodeBlock');
const InvokationContext = require('../classes/InvokationContext');
const template = require('../utils/renderTemplate');

module.exports = {
	name: 'template',
	async execute(message, args, client) {
		const context = await (new InvokationContext(message)).getContext();
		const code = removeCodeBlock(args.join(' '));
		message.channel.send(template(code, context));
	},
	module: 'Утилиты',
	description: 'Запуск шаблона сообщения',
	usage: 'template <код>',
	aliases: ['шаблон', 'hbs'],
	permissions: ['ADMINISTRATOR'],
};