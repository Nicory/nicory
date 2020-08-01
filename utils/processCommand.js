const Discord = require('discord.js');
const { prefix: defPrefix } = require('../config.json');
const db = require('../utils/database.js');
const canRun = require('../utils/canRun');

const cooldowns = new Discord.Collection();

const escapeRegex = (str) => str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

module.exports = async (message, client) => {
	const prefix = await db.get(message.guild.id, 'prefix', defPrefix);

	const prefixRegex = new RegExp(
		`^(<@!?${client.user.id}>|${escapeRegex(prefix)})\\s*`,
	);
	if (!prefixRegex.test(message.content)) return;

	if (message.author.bot) return;

	const [, matchedPrefix] = message.content.match(prefixRegex);
	const args = message.content.slice(matchedPrefix.length).trim().split(/ +/);
	const commandName = args.shift().toLowerCase();

	const command =
    client.commands.get(commandName) ||
    client.commands.find(
    	(cmd) => cmd.aliases && cmd.aliases.includes(commandName),
    );

	if (!command) return;

	if (!message.guild) return;

	if (command.args && !args.length) {
		let reply = `Ты привел неверные аргументы, ${message.author}!`;

		if (command.usage) {
			reply += `\nПравильное использование: \`${prefix}${command.name} ${command.usage}\``;
		}

		return message.channel.send(reply);
	}

	if (!cooldowns.has(command.name)) {
		cooldowns.set(command.name, new Discord.Collection());
	}

	const now = Date.now();
	const timestamps = cooldowns.get(command.name);
	const cooldownAmount = (command.cooldown || 1) * 1000;

	if (timestamps.has(message.author.id)) {
		const expirationTime = timestamps.get(message.author.id) + cooldownAmount;

		if (now < expirationTime) {
			const timeLeft = (expirationTime - now) / 1000;
			return message.reply(
				`подожди еще ${timeLeft.toFixed(
					1,
				)} секунд перед использование команды \`${command.name}\`!`,
			);
		}
	}

	timestamps.set(message.author.id, now);
	setTimeout(() => timestamps.delete(message.author.id), cooldownAmount);

	if (!await canRun(command, message)) {
		return message.reply('у вас нет прав на запуск этой команды!');
	}

	try {
		await command.execute(message, args, client);
	}
	catch (error) {
		console.error(error);
		if (error instanceof Discord.DiscordAPIError) {
			return message.reply(
				'API ошибка!\nЭто могло произойти по нескольким причинам:\n* У бота нет прав(самое частое)\n* Баги discord.js',
			);
		}
		message.reply('произошла ошибка во время запуска команды!');
	}

	console.log(
		`Executed command ${commandName} by ${message.author.tag}(${message.author.id}) in guild ${message.guild.name}(${message.guild.id}) with following message(${message.id}): ${message.content}`,
		false,
	);
};