const Discord = require('discord.js')
const db = require('../utils/database.js')

module.exports = client => {
  client.on("message", message => {

    if (message.guild==undefined) {
        return
    }
    
    await db.get(`${message.guild.id}_${message.author.id}`, 'money', parseInt(0));
    

  });
};