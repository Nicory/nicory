module.exports = {
    name: "8balls",
    hidden: false,
    module: "Веселости",
    description: "Задать вопрос боту",
    aliases: ['balls', 'Balls', 'Шар', 'шар'],
    usage: "шар <ваш вопрос>",
    cooldown: 2,
    args: false,
    async execute(message, args, client){
      const Discord = require('discord.js');
      if (args[0]==undefined) {
        return await message.reply(' укажите ваш вопрос!')
      }

      let answers=['Да', 'Нет', 'Хм... Наверное да', 'Хм... Наверное нет', 'Не знаю сама...', 'Что за глупый вопрос?', 'На какой ответ ты расчитываешь?', 'Отстань!']

      const answer = answers[Math.floor(Math.random()*answers.length)];

      await message.reply(answer)

    },
  };