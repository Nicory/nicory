db = require "../utils/database.coffee"

r = -> Math.random().toString(16).split(".")[1]

module.exports = 
  name: "token"
  execute: (message, args, client) ->  
    token = r()
    await db.set(message.guild.id, "token", token)
    message.author.send("Ваш токен доступа для вебпанели(https://nicory.xyz/dashboard) сервера `#{message.guild.name}`: ||#{token}||").then(() ->
      message.reply "ваш токен был отправлен в ЛС!\nВсе предыдущие токены этого сервера были сброшены"
    ).catch -> message.reply "у вас закрыты личные сообщения, невозможно отправить токен!"

    

  module: "Утилиты"
  description: "Получить токен доступа к панели управления"
  usage: "token"
  aliases: ["токен", "control"]
  permissions: ["ADMINISTRATOR"]