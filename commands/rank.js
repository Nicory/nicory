const htmlToImage = require('node-html-to-image');
const db = require('../utils/database.js');
const lvlUtils = require('../utils/levelsUtils.js');
const fs = require('fs');
const Handlebars = require('handlebars');
const config = require('../config.json');
const path = require('path');
const getMember = require('../utils/getMember.js');

module.exports = {
	name: 'rank',
	async execute(message, args, client) {
		let userId = getMember(args[0]);
		if (!userId) {
			userId = message.author.id;
		}

		const author = client.users.cache.get(userId);

		if (author.bot) {
			return await (message.channel.send('<:nu:732623339591303199>'));
		}

		message.channel.startTyping();

		const exp = await db.get(`${message.guild.id}_${message.author.id}`, 'exp', 0);

		const templateContent = fs
			.readFileSync(path.join(process.cwd(), 'assets', 'card.hbs'))
			.toString();
		const template = Handlebars.compile(templateContent);

		const context = {
			avatar: author.avatarURL(),
			tag: author.tag,
			exp,
			lvl: lvlUtils.getLevelFromExp(exp),
		};

		const buf = await htmlToImage({ html: template(context), transparent: true });
		message.channel.stopTyping();
		return message.channel.send({ files: [buf] });
	},

	module: 'Уровни',
	description: 'Узнать уровень юзера!',
	usage: 'ping [пользователь]',
	aliases: ['ранг', 'ранк'],
	cooldown: 10,
};
