const start = new Date();
const fs = require("fs");
const Discord = require("discord.js");
const { token, presence } = require("./config.json");
const processCommand = require("./utils/processCommand");
const loadProps = require("./utils/loadProps");

console.log(fs.readFileSync("./assets/banner.txt").toString() + "\n");

require("./utils/logging")();

const client = new Discord.Client({ 
  fetchAllMembers: true,
  messageCacheMaxSize: 1000,
  messageCacheLifetime: 30,
  messageSweepInterval: 60,
  presence,
  shardCount: 1
});
client.commands = new Discord.Collection();
client.modules = {};

client.props = loadProps();

require("./utils/loadCommands")(client);

client.once("ready", () => {
  console.log(`logged in to Discord as ${client.user.tag}`);
});

client.on("shardReady", shard => console.log(`shard ${shard} is ready`));
client.on("shardError", (err, shard) => console.log(`shard ${shard} has thrown an error: ${err}`));
client.on("shardReconnecting", (shard) => console.log(`shard ${shard} is back`));
client.on("shardDisconnect", (event, shard) => console.log(`shard ${shard} closed with ${event} event`));

client.on("message", async (message) => {
  await processCommand(message, client);
});

client.on("messageUpdate", async (_, newMsg) => {
  await processCommand(newMsg, client);
});

require("./events/expEvent.js")(client);
require("./events/onJoin")(client);
require("./events/logs.js")(client);
const end = new Date();
console.log(`bot loaded in ${end - start}ms`);

client.login(token).then(() => {
  console.log(`bot logged in and ready to go in ${new Date() - start}ms`);
});

module.exports = client;

const Backend = require("./backend/index.js");
new Backend(client);
