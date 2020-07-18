module.exports = {
    name: "random",
    hidden: false,
    module: "Веселости",
    description: "Выберет рандомное число",
    aliases: ['ранд', 'Ранд', 'Rand', 'рандом', 'Рандом', 'Random' ],
    usage: "ранд <число>",
    cooldown: 0,
    args: false,
    async execute(message, args, client){
      if (args[0]==undefined) {
        return await message.reply(' укажите цифру!')
      }
      await message.reply(' Тест')
    },
  };