/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const config = require("../config.json");
const db = require("../utils/database.js");

const randint = (min, max) =>
  Math.round(min - 0.5 + Math.random() * (max - min + 1));

module.exports = function (client) {
  const event = function (message) {
    if (!message.guild) {
      return;
    }

    if (message.author.bot) {
      return;
    }

    const totalExp = await(
      db.get(`${message.guild.id}_${message.author.id}`, "exp", 0)
    );

    const given = totalExp + randint(10, 25);

    return db.set(`${message.guild.id}_${message.author.id}`, "exp", given);
  };

  // event
  return client.on("message", event);
};
