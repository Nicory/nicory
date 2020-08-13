const db = require("../utils/database.js");

const randint = (min, max) =>
  Math.round(min - 0.5 + Math.random() * (max - min + 1));

module.exports = function(client) {
  const event = async function(message) {
    if (!message.guild) {
      return;
    }

    if (message.author.bot) {
      return;
    }

    const totalExp = await db.get(`${message.guild.id}_${message.author.id}`, "exp", 0);

    const given = totalExp + randint(10, 25);

    return db.set(`${message.guild.id}_${message.author.id}`, "exp", given);
  };

  // event
  return client.on("message", event);
};
