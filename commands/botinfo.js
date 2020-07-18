module.exports = {
    name: "botinfo",
    module: "Основное",
    description: "Информация про бота",
    aliases: ["бот", "ботинфо", "bot"],
    usage: "botinfo",
    args: false, 
    async execute(message, args, client){
        const Discord = require('discord.js');
        const package = require("../package.json")
        const config = require("../config.json")
        const embed = new Discord.MessageEmbed()
        .setColor('#e155ff')
        .setTitle('Nicory Bot')
        .setAuthor('Информация про бота')
        .setDescription('Nicory это мультисерверный Discord бот с различным функционалом, от обычной модерации до полноценной системы логирования, экономики и системы уровней')
        .setThumbnail(client.user.avatarURL())
        .addFields(
            {name: 'Мои создатели:', value: '<a:neloext3:732991861387689984> NeloExt3#3100, \n<a:kislball:732991861177712760> KislBall#9017', inline: true},
            { name: 'Я написана на:', value: 'CoffeeScript\nJavaScript', inline: true },
            {name: "Мои библеотеки:", value: Object.keys(package.dependencies).join("\n"), inline: true}, 
            {name: 'Серверная информация:', value: `Префикс: ${config.prefix}\n`, inline: false},
            {name: 'Версия:', value: `${package.version} [${config.date}] Debug`, inline: false},
            {name: 'Я нахожусь на:', value: `${client.guilds.cache.size} серверах!`},
            {name: 'Пинг', value: `${message.client.ws.ping} мс!`},
            {name: 'Сервер технической поддержки:', value: 'https://discord.gg/GND9y4e', inline: true},
            {name: 'Сайт бота:', value: 'https://nicory.xyz'}
        )
        .setFooter(`${config.copy}`, client.user.avatarURL());
        message.channel.send(embed);
    }
}