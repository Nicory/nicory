const haste = require('hastebin-gen');

module.exports = {
	name: 'edits',
	async execute(message, args, client) {
		if (!args[0]) {
			return message.reply('сообщение не найдено!');
		}
		const edits = client.channels.cache.find(c => c.type == 'text' && c.messages.cache.has(args[0]))?.messages.cache.get(args[0])?.edits;
		if (!edits) {
			return message.reply('сообщение не найдено!');
		}
		message.reply(await haste(edits.map(e => e.content).join('\n')));
	},
	module: 'Утилиты',
	description: 'Просмотреть историю изменений сообщения',
	usage: 'edits <айди сообщения>',
	aliases: ['изменения', 'эдиты'],
	cooldown: 10,
};
