module.exports = {
  name: "serverinfo",
  module: "Основное",
  description: "Информация про сервер",
  aliases: ["сервер", "серверинфо", "server"],
  usage: "serverinfo",
  args: false,
  async execute(message, _, client) {
    const Discord = require("discord.js");

    const online = message.guild.members.cache.filter(c => c.presence.status == "online").size;
    const idle = message.guild.members.cache.filter(c => c.presence.status == "idle").size;
    const dnd = message.guild.members.cache.filter(c => c.presence.status == "dnd").size;
    const offline = message.guild.members.cache.filter(c => c.presence.status == "offline").size;
    const text = message.guild.channels.cache.filter(c => c.type == "text").size;
    const voice = message.guild.channels.cache.filter(c => c.type == "voice").size;

    const embed = new Discord.MessageEmbed()
      .setColor("#e155ff")
      .setTitle(`${message.guild.name}`)
      .setAuthor("Информация про сервер")
      .setDescription(`Информация про сервер ${message.guild.name}`)
      .setThumbnail(message.guild.iconURL())
      .addFields(
        { name: "Информация:", value: `⏳ Сервер создан: ${message.guild.createdAt.toLocaleString()} \n👑 Создатель сервера: ${message.guild.owner} \nРегион: кислый тута сделаешь` },
        { name: "Участники:", value: ` Всего участников:${message.guild.members.cache.size} \n<:online:728682549819473970> В онлайне: ${online}, \n<:idle:728682549890515094> Отошли: ${idle}, \n<:dnd:728682911057838140> Не беспокоить: ${dnd}, \n<:9819_Offline:728682548280033281> Оффлайн: ${offline}` },
        { name: "Каналы", value: `🧭 Всего каналов: ${message.guild.channels.cache.size}, \n📝 Текстовых каналов: ${text}, \n🔊 Голосовых каналов: ${voice}` },
      )
      .setFooter(`${message.guild.id}`, client.user.avatarURL());
    message.channel.send(embed);
  },
};