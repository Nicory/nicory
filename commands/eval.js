/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const util = require('util');
const db = require('../utils/database.js');

module.exports = {
	name: 'eval',
	async execute(message, args, client) {
		if (
			['419524085736013834', '622747295435456512'].includes(message.author.id)
		) {
			let evaled = '';
			try {
				evaled = await (eval(args.join(' ')));
				return message.channel.send(evaled);
			}
			catch (error) {
				return message.reply('there was an error during evaluation.\n' + error);
			}
		}
	},

	hidden: true,
	usage: 'ping',
	aliases: ['js'],
};
