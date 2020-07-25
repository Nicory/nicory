/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
module.exports = { 
  name: "ping",
  execute(message, args, client) {  
    return await(message.channel.send(`:ping_pong: Pong!\n\`${message.client.ws.ping}ms\`\nPS: Это первая команда, которая была написана на CoffeeScript`));
  },
  module: "Основное",
  description: "Пинг бота до серверов Discord",
  usage: "ping",
  aliases: ["пинг"]
};