const Discord = require('discord.js');
const db = require('../utils/database.js');
const { get } = require('../utils/database.js');
let logChannel

module.exports = client => {
	client.on('messageDelete', async message => {
    
    // Получение канала для логов из бд
    const getID = await db.get(`${message.guild.id}`, 'logChannel')
    logChannel=message.guild.channels.cache.get(getID)


		if (message.author.bot) {
			return;
    }

    if (message.content==null || undefined) {
      return;
    }
    
    const embed = new Discord.MessageEmbed()
    .setAuthor('Сообщание было удалено!')
    .setDescription('**Содержание сообщения**\n' + `\`\`\`${message.content}\`\`\` `)
    .setColor('#e155ff')
    .addField(
      'Автор',
      message.author,
      true
    )
    .addField(
      'Канал',
      message.channel,
      true
    )
    .setFooter(`ID сообщения: ${message.id} || ID автора: ${message.author.id}`);
    logChannel.send(embed)

  });
  client.on('messageUpdate', async (oldMessage, newMessage) => {

		if (newMessage.author.bot) {
			return;
    }

    // Получение канала для логов из бд
    const getID = await db.get(`${newMessage.guild.id}`, 'logChannel')
    logChannel=newMessage.guild.channels.cache.get(getID)

    const embed = new Discord.MessageEmbed()
    .setAuthor('Сообщание было изменено!')
    .setDescription('**Содержание старого сообщения**\n' + `\`\`\`${oldMessage.content}\`\`\` ` + '**Содержание старого сообщения**\n' + `\`\`\`${newMessage.content}\`\`\` `)
    .setColor('#e155ff')
    .addField(
      'Автор',
      newMessage.author,
      true
    )
    .addField(
      'Канал',
      newMessage.channel,
      true
    )
    .setFooter(`ID сообщения: ${newMessage.id} || ID автора: ${newMessage.author.id}`);

    logChannel.send(embed)
  });
};