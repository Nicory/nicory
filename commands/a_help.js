const { MessageEmbed } = require("discord.js");
const config = require("../config.json");

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

module.exports = {
  name: "help",
  async execute(message, args, client) {
    const embed = new MessageEmbed()
      .setColor(0xe155ff)
      .setTitle("Помощь по командам")
      .setThumbnail(client.user.avatarURL())
      .setFooter("By: KislBall and NeloExt3", client.user.avatarURL());
    if (!args[0]) { // sending main help
      for (const moduleName in client.modules) {
        const mdl = client.modules[moduleName];
        let content = "";
        for (const command of mdl) {
          content += "`" + config.prefix + command.name + "` "
        }
        embed.addField(`${moduleName}(${config.prefix}help ${moduleName})`, content);
      }
    } else { // sending module specific help
      const moduleName = capitalizeFirstLetter(args[0]);
      if (!client.modules[moduleName]) return message.react("❌");
      embed.setTitle(`Команды модуля ${moduleName}`);
      const mdl = client.modules[moduleName];
      
      for (const command of mdl) { 
        const aliases = command.aliases;
        embed.addField(
          `${config.prefix}${command.name}`,
          `${command.description ? command.description : "<нет информации>"}\n\n**Использование**: \`${
            command.usage ? command.usage : "<нет информации>"
          }\`\n**Алиасы**: ${aliases.map(a => '`' + a + '`').join(" ")}`
        );
      }
    }
    message.channel.send(embed);
  },
  module: "Основное",
  description: "Справка по командам",
  usage: "help [модуль]",
  aliases: ["хелп"],
};