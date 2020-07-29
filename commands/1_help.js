const { MessageEmbed } = require('discord.js');
const config = require('../config.json');
const db = require('../utils/database');

const translations = {
	'ADMINISTRATOR': 'Администратор',
	'CREATE_INSTANT_INVITE': 'Создавать приглашения',
	'KICK_MEMBERS': 'Выгонять участников',
	'BAN_MEMBERS': 'Банить участников',
	'MANAGE_CHANNELS': 'Управлять каналами',
	'MANAGE_GUILD': 'Управлять сервером',
	'ADD_REACTIONS': 'Добавлять реакции',
	'VIEW_AUDIT_LOG': 'Просматривать журнал аудита',
	'PRIORITY_SPEAKER': 'Приоритетный режим',
	'STREAM': 'Видео',
	'VIEW_CHANNEL': 'Читать текстовые каналы и видеть голосовые каналы',
	'SEND_MESSAGES': 'Отправлять сообщения',
	'SEND_TTS_MESSAGES': 'Отправлять TTS сообщения',
	'MANAGE_MESSAGES': 'Управлять сообщениями',
	'EMBED_LINKS': 'Встраивать ссылки',
	'ATTACH_FILES': 'Прикреплять сообщения',
	'READ_MESSAGE_HISTORY': 'Читать историю сообщений',
	'MENTION_EVERYONE': 'Упоминать все роли',
	'USE_EXTERNAL_EMOJIS': 'Использовать внешние эмодзи',
	'CONNECT': 'Подключаться к голосовым каналам',
	'SPEAK': 'Говорить',
	'USE_VAD': 'Режим активации по голосу',
	'CHANGE_NICKNAME': 'Изменять свой никнейм',
	'MANAGE_NICKNAMES': 'Управлять никнеймами',
	'MANAGE_ROLES': 'Управлять ролями',
	'MANAGE_WEBHOOKS': 'Управлять вебхуками',
	'MANAGE_EMOJIS': 'Управлять эмодзи',
};

function capitalizeFirstLetter(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}

function perms(command) {
	const perm = command.permissions;
	if (!perm) return '';
	return `**Права для запуска команды**: ${capitalizeFirstLetter((perm.map(el => '`' + translations[el] + '`').join(' ')).toLowerCase())}`;
}

module.exports = {
	name: 'help',
	async execute(message, args, client) {
		const prefix = await db.get(message.guild.id, 'prefix', config.prefix);

		const embed = new MessageEmbed()
			.setColor(0xe155ff)
			.setTitle('Помощь по командам')
			.setThumbnail(client.user.avatarURL())
			.setFooter('By: KislBall and NeloExt3', client.user.avatarURL())
			.setDescription(`Мой префикс здесь - \`${prefix}\`, но также вы можете @упомянуть меня.\nВы можете сменить префикс командой \`prefix\``);
		if (!args[0]) { // sending main help
			for (const moduleName in client.modules) {
				const mdl = client.modules[moduleName];
				let content = '';
				for (const command of mdl) {
					content += '`' + prefix + command.name + '` ';
				}
				embed.addField(`${moduleName}(${prefix}help ${moduleName})`, content);
			}
		}
		else { // sending module specific help
			const moduleName = capitalizeFirstLetter(args[0]);
			if (!client.modules[moduleName]) return message.react('❌');
			embed.setTitle(`Команды модуля ${moduleName}`);
			const mdl = client.modules[moduleName];

			for (const command of mdl) {
				const aliases = command.aliases;
				embed.addField(
					`${prefix}${command.name}`,
					`${command.description ? command.description : '<нет информации>'}\n\n**Использование**: \`${
						command.usage ? command.usage : '<нет информации>'
					}\`\n**Алиасы**: ${aliases.map(a => '`' + a + '`').join(' ')}\n**Кулдаун**: ${command.cooldown || 0}s\n${perms(command)}`,
				);
			}
		}
		message.channel.send(embed);
	},
	module: 'Основное',
	description: 'Справка по командам',
	usage: 'help [модуль]',
	aliases: ['хелп'],
};