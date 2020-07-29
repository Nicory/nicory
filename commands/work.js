/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const db = require('../utils/database.js');
const config = require('../config.json');
const _ = require('lodash');

module.exports = {
	name: 'work',
	async execute(message, args, client) {
		const jobs = await (db.get(`${message.guild.id}`, 'customJobs', []));

		if (!args[0]) {
			return await message.reply('укажите работу!\nСписок доступных работ можно увидеть по команде: `jobs`');

		}

		if (jobs.filter((el) => el.name === args[0]).length === 0) {
			return await message.reply('эта работа не найдена!\nСписок доступных работ можно увидеть по команде: `jobs`');
		}

		const job = jobs.filter((el) => el.name === args[0])[0];
		const salary = _.random(parseInt(job.min), parseInt(job.max));

		const oldBalance = await db.get(`${message.guild.id}_${message.author.id}`, 'money', 0);
		const newBalance = salary + oldBalance;

		return db
			.set(`${message.guild.id}_${message.author.id}`, 'money', newBalance)
			.then(() =>
				message.channel.send(
					`${message.author} работает на работе \`${args[0]}\` и получает ${salary} кредитов!`,
				),
			);
	},

	module: 'Экономика',
	description: 'Зарабатывать деньги на работе',
	usage: 'work <название работы>',
	aliases: ['работать'],
};
