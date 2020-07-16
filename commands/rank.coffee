htmlToImage = require "node-html-to-image"
mongodb = require "mongodb"
lvlUtils = require "../utils/levelsUtils.coffee"
fs = require "fs"
Handlebars = require "handlebars"
config = require "../config.json"
path = require "path"
getMember = require "../utils/getMember.js"

module.exports = 
  name: "rank"
  execute: (message, args, client) ->  
    conn = await mongodb.MongoClient.connect(config.mongo)
    col = conn.db("nicory").collection "user_exp"

    userId = getMember args[0]
    if !userId
      userId = message.author.id

    author = client.users.cache.get userId

    data = await col.findOne {guild: message.guild.id, member: author.id} 
    
    templateContent = fs.readFileSync(path.join(process.cwd(), "assets", "card.hbs")).toString()
    template = Handlebars.compile templateContent

    context = {
      avatar: author.avatarURL(),
      tag: author.tag,
      exp: data.exp || 0,
      lvl: lvlUtils.getLevelFromExp data.exp || 0
    }

    buf = await htmlToImage({html: template(context), transparent: true})
    message.channel.send({files: [buf]})

  module: "Уровни"
  description: "Узнать уровень юзера!"
  usage: "ping [пользователь]"
  aliases: ["ранг", "ранк"]