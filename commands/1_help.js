const { MessageEmbed } = require("discord.js");
const config = require("../config.json");
const db = require("../utils/database");
const canRun = require("../utils/canRun");

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function perms(command, lang = "ru") {
  const {props} = require("../index");
  const translations = props[`nicory.${lang}.permissions`];
  const perm = command.permissions;
  if (!perm) return "";
  return `**Права для запуска команды**: ${capitalizeFirstLetter((perm.map(el => "`" + translations[el] + "`").join(" ")).toLowerCase())}`;
}

module.exports = {
  name: "help",
  async execute(message, args, client) {
    const prefix = await db.get(message.guild.id, "prefix", config.prefix);

    const embed = new MessageEmbed()
      .setColor(0xe155ff)
      .setTitle("Помощь по командам")
      .setThumbnail(client.user.avatarURL())
      .setFooter("By: KislBall and EnotKEK3", client.user.avatarURL())
      .setDescription(`Мой префикс здесь - \`${prefix}\`, но также вы можете @упомянуть меня.\nВы можете сменить префикс командой \`prefix\`\nВсего команд: **${client.commands.size}**`);
    try {
      if (!args[0]) { // sending main help
        for (const moduleName in client.modules) {
          const mdl = client.modules[moduleName];
          let content = "";
          for (const command of mdl) {
            if (!await canRun(command, message)) continue;
            content += "`" + prefix + command.name + "` ";
          }
          embed.addField(`${moduleName}(${prefix}help ${moduleName})`, content);
        }
      }
      else { // sending module specific help
        const moduleName = capitalizeFirstLetter(args[0]);
        if (!client.modules[moduleName]) return message.react("❌");
        embed.setTitle(`Команды модуля ${moduleName}`);
        const mdl = client.modules[moduleName];

        for (const command of mdl) {
          if (!await canRun(command, message)) continue;
          const aliases = command.aliases;
          embed.addField(
            `${prefix}${command.name}`,
            `${command.description ? command.description : "<нет информации>"}\n\n**Использование**: \`${
              command.usage ? command.usage : "<нет информации>"
            }\`\n**Алиасы**: ${aliases.map(a => "`" + a + "`").join(" ")}\n**Кулдаун**: ${command.cooldown || 0}s\n${perms(command)}`,
          );
        }
      }
    }
    catch (e) {
      "";
    }
    message.channel.send(embed);
  },
  module: "Основное",
  description: "Справка по командам",
  usage: "help [модуль]",
  aliases: ["хелп"],
};