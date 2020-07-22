util = require "util"
db = require "../utils/database.coffee"

module.exports = 
  name: "eval"
  execute: (message, args, client) ->  
    if ["419524085736013834", "622747295435456512"].includes message.author.id
      evaled = ""
      try 
        evaled = await eval(args.join(' '))
        message.channel.send(evaled)

      catch error 
        message.reply('there was an error during evaluation.\n' + error)
    
  hidden: true
  usage: "ping"
  aliases: ["js"]