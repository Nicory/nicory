module.exports = {
  name: "ping",
  async execute(message, args, client) { 
    await message.channel.send(`:ping_pong: Pong!\n\`${message.client.ws.ping}ms\``);
  },
  module: "Основное",
  description: "Пинг бота до серверов Discord",
  usage: "ping",
  aliases: ["пинг"]
};