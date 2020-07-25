const ms = require('ms');
const haste = require('hastebin-gen');

function getHasteLink(usage) {
	let str = `Кучей занято: ${usage.heapTotal / 1024 / 1024}MB\n`;
	str += `Кучей использовано: ${usage.heapUsed / 1024 / 1024}MB\n`;
	str += `Используется внешними источниками NodeJS(объекты C++ и тд): ${
		(usage.external - usage.arrayBuffers) / 1024 / 1024
	}MB\n`;
	str += `Занято бинарными массивами: ${usage.arrayBuffers / 1024 / 1024}MB\n`;
	str += `============\nИтого: ${usage.rss / 1024 / 1024}MB`;
	return haste(str, { extension: 'txt' });
}

module.exports = {
	name: 'botinfo',
	module: 'Основное',
	description: 'Информация про бота',
	aliases: ['бот', 'ботинфо', 'bot'],
	usage: 'botinfo',
	args: false,
	async execute(message, args, client) {
		const Discord = require('discord.js');
		const package = require('../package.json');
		const config = require('../config.json');
		const embed = new Discord.MessageEmbed()
			.setColor('#e155ff')
			.setTitle('Nicory Bot')
			.setAuthor('Информация про бота')
			.setDescription(
				'Nicory это мультисерверный Discord бот с различным функционалом, от обычной модерации до полноценной системы логирования, экономики и системы уровней',
			)
			.setThumbnail(client.user.avatarURL())
			.addFields(
				{
					name: 'Мои создатели:',
					value:
                'NeloExt3#3100\nKislBall#9017',
					inline: true,
				},
				{
					name: 'Я написана на:',
					value: 'JavaScript',
					inline: true,
				},
				{
					name: 'Мои библеотеки:',
					value: Object.keys(package.dependencies).join('\n'),
					inline: true,
				},
				{
					name: 'Серверная информация:',
					value: `Префикс: ${config.prefix}\n`,
					inline: false,
				},
				{
					name: 'Версия:',
					value: `${package.version} [${config.date}] Debug`,
					inline: false,
				},
				{
					name: 'Я нахожусь на:',
					value: `${client.guilds.cache.size} серверах!`,
				},
				{ name: 'Пинг', value: `${message.client.ws.ping} мс!`, inline: true },
				{
					name: 'Аптайм:',
					value: ms(client.uptime),
					inline: true,
				},
				{
					name: 'Использование ОЗУ:',
					value: `${
						(process.memoryUsage().heapUsed / 1024 / 1024).toFixed(1)
					}MB\nА информацию для задротов можно узнать [здесь](${await getHasteLink(
						process.memoryUsage(),
					)})`,
					inline: true,
				},
				{
					name: 'Сервер технической поддержки:',
					value: 'https://discord.gg/GND9y4e',
					inline: true,
				},
				{ name: 'Сайт бота:', value: 'https://nicory.xyz' },
			)
			.setFooter(`${config.copy}`, client.user.avatarURL());
		message.channel.send(embed);
	},
};