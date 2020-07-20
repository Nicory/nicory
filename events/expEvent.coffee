config = require "../config.json"
db = require "../utils/database.coffee"

randint = (min, max) -> Math.round min - 0.5 + Math.random() * (max - min + 1)

module.exports = (client) ->
  event = (message) ->
    if !message.guild
      return

    if message.author.bot
      return

    totalExp = await db.get("#{message.guild.id}_#{message.author.id}", "exp", 0)

    given = totalExp + randint(10,25)

    db.set("#{message.guild.id}_#{message.author.id}", "exp", given)




  # event
  client.on("message", event)