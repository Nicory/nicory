module.exports = {
  name: "Shop",
  hidden: false,
  module: "Экономика",
  description: "Покажет магазин сервера",
  aliases: [ 'shop', 'магаз', 'Магаз', 'магазин', 'Магазин', ],
  usage: "shop",
  cooldown: 2,
  args: false,
  async execute(message, args, client){
    const Discord = require('discord.js')
    const db = require('../utils/database.js')
    const getRol = require('../utils/getRole')

		const roles = await (db.get(message.guild.id, 'shop', []));
		const embed = new Discord.MessageEmbed()
			.setColor(0xe155ff)
			.setThumbnail(message.guild.iconURL())
			.setTitle(`Магазин сервера ${message.guild.name}`);
		if (roles.length === 0) {
			embed.setDescription(
				'Магазин пуст!',
			);
			return await (message.channel.send(embed));
		}

		for (const role of Array.from(roles)) {
      const rol = getRol(role.role)
      const apiRole = message.guild.roles.cache.get(rol).name
			embed.addField(apiRole, `${role.price}`);
		}

		return message.channel.send(embed);
	},

};