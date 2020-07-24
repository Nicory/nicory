db = require "../utils/database.coffee"
config = require "../config.json"
_ = require "lodash"


module.exports = 
  name: "work"
  execute: (message, args, client) ->  
    jobs = await db.get("#{message.guild.id}", "customJobs", [])

    if !args[0]
      return await message.reply "укажите работу!\nСписок доступных работ можно увидеть по команде: `#{config.prefix}jobs`"

    if jobs.filter((el) -> el.name == args[0]).length == 0
      return await message.reply "эта работа не найдена!\nСписок доступных работ можно увидеть по команде: `#{config.prefix}jobs`"

    job = jobs.filter((el) -> el.name == args[0])[0]
    salary = _.random(parseInt(job.min), parseInt(job.max))

    oldBalance = await db.get("#{message.guild.id}_#{message.author.id}", 'money', 0)
    newBalance = salary + oldBalance

    db.set("#{message.guild.id}_#{message.author.id}", 'money', newBalance).then () -> 
      message.channel.send "#{message.author} работает на работе `#{args[0]}` и получает #{salary} кредитов!"

  module: "Экономика"
  description: "Зарабатывать деньги на работе"
  usage: "work <название работы>"
  aliases: ["работать"]