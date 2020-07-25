/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
module.exports = {
	name: 'ping',
	async execute(message, args, client) {
		return await (message.channel.send(`:ping_pong: Pong!\n\`${message.client.ws.ping}ms\``));
	},
	module: 'Основное',
	description: 'Пинг бота до серверов Discord',
	usage: 'ping',
	aliases: ['пинг'],
};