const fs = require("fs");
const Discord = require("discord.js");
const { token } = require("./config.json");
const processCommand = require("./utils/processCommand");

console.log(fs.readFileSync("./assets/banner.txt").toString() + "\n");

require("./utils/logging")();

const client = new Discord.Client({ fetchAllMembers: true });
client.commands = new Discord.Collection();
client.modules = {};

require("./utils/loadCommands")(client);

client.once("ready", () => {
  console.log(`Logged in to Discord as ${client.user.tag}`);
});

client.on("message", async (message) => {
  await processCommand(message, client);
});

client.on("messageUpdate", async (oldMsg, newMsg) => {
  await processCommand(newMsg, client);
});

require("./events/expEvent.js")(client);
require("./events/onJoin")(client);
require("./events/logs.js")(client);

client.login(token);

module.exports = client;

const Backend = require("./backend/index.js");
new Backend(client);
