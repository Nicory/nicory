const htmlToImage = require("node-html-to-image");
const removeCodeBlock = require("../utils/removeCodeBlock");

module.exports = {
  name: "html",
  async execute(message, args) {
    message.channel.startTyping();
    const code = removeCodeBlock(args.join(" "));
    const buffer = await (htmlToImage({ html: code, transparent: true }));
    await (message.channel.send({ files: [buffer] }));
    return message.channel.stopTyping();
  },
  module: "Утилиты",
  description: "Отрисовать HTML",
  usage: "html <код>",
  aliases: ["хтмл", "веб"],
  cooldown: 5,
};