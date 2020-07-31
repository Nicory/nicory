const removeCodeBlock = require("../utils/removeCodeBlock");
const InvokationContext = require("../classes/InvokationContext");
const Handlebars = require("handlebars");

module.exports = {
  name: 'template',
  async execute(message, args, client) {
    const context = await (new InvokationContext(message)).getContext();
    const code = removeCodeBlock(args.join(" "));
    const tmpl = Handlebars.compile(code);
    message.channel.send(tmpl(context));
  },
  module: 'Утилиты',
  description: 'Запуск шаблона сообщения',
  usage: 'template <код>',
  aliases: ['шаблон', 'hbs'],
  permissions: ["ADMINISTRATOR"]
};