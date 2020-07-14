module.exports = {
  name: "ping",
  hidden: true,
  async execute(message, args) { 
    await message.reply(`:ping_pong: Pong!\n\`${message.client.ws.ping}ms\``);
  }
};