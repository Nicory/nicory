module.exports = 
  name: "warns"
  execute: (message, args, client) ->  
    await message.channel.send ":ping_pong: Pong!\n`#{message.client.ws.ping}ms`\nPS: Это первая команда, которая была написана на CoffeeScript"
  module: "Основное"
  description: "Пинг бота до серверов Discord"
  usage: "ping"
  aliases: ["преды", "варны"]