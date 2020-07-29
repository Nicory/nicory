const Discord = require('discord.js');
const db = require('../utils/database.js');
const { get } = require('../utils/database.js');

module.exports = client => {
	client.on('messageDelete', async message => {
    
    // Получение канала для логов из бд
    const getID = await db.get(`${message.guild.id}`, 'logChannel')
    const logChannel = message.guild.channels.cache.get(getID)


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
    const logChannel = newMessage.guild.channels.cache.get(getID)
    
    if (!logChannel) return;

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

  client.on('guildMemberAdd', async member => {
    // Получение канала для логов из бд
    const getID = await db.get(`${member.guild.id}`, 'logChannel')
    const logChannel = member.guild.channels.cache.get(getID)
    
    if (!logChannel) return;

    const embed = new Discord.MessageEmbed()
    .setAuthor('На сервер зашёл участник!')
    .setDescription(`${member}`)
    .setFooter(`ID ${member.id}`)
    .setTimestamp()
    logChannel.send(embed)
  });

  client.on('guildMemberRemove', async member => {
    // Получение канала для логов из бд
    const getID = await db.get(`${member.guild.id}`, 'logChannel')
    const logChannel = member.guild.channels.cache.get(getID)
    
    if (!logChannel) return;

    const embed = new Discord.MessageEmbed()
    .setAuthor('Участник покинул сервер!')
    .setDescription(`${member}`)
    .setFooter(`ID ${member.id}`)
    .setTimestamp()
    logChannel.send(embed)
  });

  client.on("nicory_warn", async warn => { 
    const getID = await db.get(`${warn.user.guild.id}`, 'logChannel')
    const logChannel = warn.user.guild.channels.cache.get(getID);

    if (!logChannel) return;

    const embed = new Discord.MessageEmbed()
      .setAuthor("Выдано предупреждение")
      .setDescription(`${warn.reason}`)
      .setFooter(`ID ${warn.id} | Moder ID ${warn.moderator}`)
      .addField(`Участник:`, warn.user.toString() + " | " + warn.user.user.id)
      .setTimestamp();
    logChannel.send(embed);    
  });

  client.on("nicory_unwarn", async (warn) => {
    const getID = await db.get(`${warn.member.guild.id}`, "logChannel");
    const logChannel = warn.member.guild.channels.cache.get(getID);

    if (!logChannel) return;

    const embed = new Discord.MessageEmbed()
      .setAuthor("Снято предупреждение")
      .setFooter(`ID ${warn.id} | Moder ID ${warn.moderator.user.id}`)
      .addField(`Участник:`, warn.member.toString() + " | " + warn.member.user.id)
      .setTimestamp();
    logChannel.send(embed);
  });
};