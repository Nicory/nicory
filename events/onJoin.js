const Discord = require('discord.js');
const { prefix } = require("../config.json");

module.exports = client => {
  client.on("guildCreate", guild => {
    const embed = new Discord.MessageEmbed()
      .setTitle('Nicory Bot')
      .setDescription(`Доброго дня!\nВы получили это сообщение так как вы являетесь создателем сервера **${guild.name}**!\nЭто чисто информативное сообщение, чтоб вы лучше понимали кто такая Nicory и что она может.`)
      .setColor('#e155ff')
      .addFields(
        {
          name: 'Основная информация', 
          value: 'Nicory это мультисерверный Discord бот с различным функционалом, с которым вы можете ознакомится по команде `!!хелп` на вашем сервере.'
        },

        {
          name: 'Основной функционал', 
          value: 'Основной функционал Nicory это: Модерация, Экономика, Кастомные команды, Система логирования.\nКак уже и говорилось, все про команды вы можете ознакомится командой `!!хелп` на вашем сервере.'
        },

        {
          name: 'Остальное',
          value: `Стандартный префикс: \`${prefix}\`\nСоздатели:\nNeloExt3#3100\nKislBall#9017\n<:discord:734506565201035264> Discord сервер бота: https://discord.gg/GND9y4e`
        }
      )
      .setFooter('Спасибо что пользуетесь Nicory Bot!', 'https://cdn.discordapp.com/avatars/706600733931339806/b414b516bcf79c9e03a74e10cbd0ceb2.webp')
    guild.owner.send(embed)
    
  });
};