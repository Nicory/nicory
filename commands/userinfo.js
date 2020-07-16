module.exports = {
    name: "userinfo",
    module: "Основное",
    description: "Информация про юзера",
    aliases: ["юзер", "юзеринфо", "user"],
    usage: "userinfo",
    args: false, 
    async execute(message, args, client){
        const Discord = require('discord.js');
        const package = require("../package.json")
        const config = require("../config.json")

        const getMember = require("../utils/getMember.js");
        if (args[0]==undefined) {
            var id=message.author.id
        } else {
            var id=getMember(args[0])
        }

        const user = message.guild.members.resolve(id)

        if (user.Nickname==null) {
            var nickname=user.displayName
        } else {
            var nickname=user.Nickname
        }

        // Чек статуса
        if (user.presence.status=='online') {
            var status='<:online:728682549819473970> Онлайн'
        } else if (user.presence.status=='idle') {
            var status='<:idle:728682549890515094> Отошёл'
        } else if (user.presence.status=='dnd') {
            var status='<:dnd:728682911057838140> Не беспокоить'
        } else if (user.presence.status=='offline') {
            var status='<:9819_Offline:728682548280033281> Оффлайн'
        } else {
            var status='Произошла ошибка!'
        }


        const embed = new Discord.MessageEmbed()
        .setColor('#e155ff')
        .setTitle(`${nickname}`)
        .setAuthor('Информация про пользователя')
        .setDescription(`Кислый тут сделаешь типа кастомный текст можно поставить о себе типа эта хуета`)
        .addFields(
            {name: 'Основная информация:', value: `Имя пользователя: ${user}\nАккаунт создан: \nПрисоединился: \nСтатус: ${status}\nИграет в: ${user.presence.activities}`},
            {name: 'Уровень', value: `Кислый когда сделаем уровни, тута сделаешь`, inline: true},
            {name: 'Баланс', value: `Кислый когда сделаем экономику, тута сделаешь`, inline: true},
            {name: 'Опыт', value: `Кислый когда сделаем уровни, тута сделаешь`, inline: true},
        )
        .setFooter(`ID: ${user.id}`)
        message.channel.send(embed);
    }
}