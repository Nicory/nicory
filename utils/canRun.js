const db = require('./database');
const Discord = require('discord.js');

module.exports = async (command, message) => {
	if (['419524085736013834', '622747295435456512'].includes(message.author.id)) return true;
	if (command.permissions) {
		let num = 0;
		for (const perm of command.permissions) {
			num = num | Discord.Permissions.FLAGS[perm];
		}

		const modRole = await db.get(message.guild.id, 'modRole', '');

		if (!message.member.permissions.has(num)) {
			if (!message.member.roles.cache.has(modRole)) {
				return false;
			}
			else if (
				message.member.roles.cache.has(modRole) &&
        command.permissions.includes('ADMINISTRATOR')
			) {
				return false;
			}
		}
	}
	return true;
};