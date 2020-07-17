module.exports = {
  name: "kick",
  hidden: false,
  module: "Модерация",
  description: "кикнуть участника",
  aliases: ["кик", 'Кик', 'Kick'],
  usage: "kick юзер причина",
  args: false,
  async execute(message, args, client){
    const getMember = require("../utils/getMember.js");

    userId = getMember(args[0])
    const user = message.guild.members.resolve(userId)
    const author = message.guild.members.resolve(message.author.id)

    if (args[0]==undefined) {
      return await message.reply(` обязательно укажите юзера!`)
    }

    if (userId==message.author.id) {
      return await message.reply(` вы не можете кикнуть самого себя!`)
    }

    if (author.roles.highest.position < user.roles.highest.position) {
      return await message.reply(` вы не можете кикнуть человека который выше вас по роли!`)
    } else if (author.roles.highest.position == user.roles.highest.position) {
      return await message.reply(` вы не можете кикнуть человека который на одинаковой с вами роли!`)
    }

    var reason=args.slice(1).join(" ")
    if (reason=="") {
      var reason='Не указана'
    }
    message.author.send(`Вы были кикнуты с сервера ${message.guild.name} модератором ${author}\nПо причине: ${reason}`)
    user.kick(reason)
    message.react('✅');

  },
  permissions: ["KICK_MEMBERS"]
};