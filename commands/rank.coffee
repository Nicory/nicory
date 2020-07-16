htmlToImage = require "node-html-to-image"
mongodb = require "mongodb"
lvlUtils = require "../utils/levelsUtils.coffee"
fs = require "fs"
Handlebars = require "handlebars"
config = require "../config.json"
path = require "path"

module.exports = 
  name: "rank"
  execute: (message, args, client) ->  
    conn = await mongodb.MongoClient.connect(config.mongo)
    col = conn.db("nicory").collection "user_exp"

    data = await col.findOne {guild: message.guild.id, member: message.author.id} 
    
    templateContent = fs.readFileSync(path.join(process.cwd(), "assets", "card.hbs")).toString()
    template = Handlebars.compile templateContent

    context = {
      avatar: message.author.avatarURL(),
      tag: message.author.tag,
      exp: data.exp || 0,
      lvl: lvlUtils.getLevelFromExp data.exp || 0
    }

    buf = await htmlToImage({html: template(context), transparent: true})
    message.channel.send({files: [buf]})

  module: "Уровни"
  description: "Узнать уровень юзера!"
  usage: "ping [пользователь]"
  aliases: ["ранг", "ранк"]