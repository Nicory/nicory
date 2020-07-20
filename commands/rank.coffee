htmlToImage = require "node-html-to-image"
db = require "../utils/database.coffee"
lvlUtils = require "../utils/levelsUtils.coffee"
fs = require "fs"
Handlebars = require "handlebars"
config = require "../config.json"
path = require "path"
getMember = require "../utils/getMember.js"

module.exports = 
  name: "rank"
  execute: (message, args, client) ->  
    userId = getMember args[0]
    if !userId
      userId = message.author.id

    author = client.users.cache.get userId

    if author.bot
      return await message.channel.send "<:nu:732623339591303199>"

    message.channel.startTyping()

    exp = await db.get("#{message.guild.id}_#{message.author.id}", "exp", 0)
    
    templateContent = fs.readFileSync(path.join(process.cwd(), "assets", "card.hbs")).toString()
    template = Handlebars.compile templateContent

    context = {
      avatar: author.avatarURL(),
      tag: author.tag,
      exp: exp,
      lvl: lvlUtils.getLevelFromExp exp
    }

    buf = await htmlToImage({html: template(context), transparent: true})
    message.channel.stopTyping()
    message.channel.send({files: [buf]})

  module: "Уровни"
  description: "Узнать уровень юзера!"
  usage: "ping [пользователь]"
  aliases: ["ранг", "ранк"]
  cooldown: 10