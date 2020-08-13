const fs = require("fs");

module.exports = client => {
  const commandFiles = fs
    .readdirSync("./commands")
    .filter((file) => file.endsWith(".js"));

  for (const file of commandFiles) {
    const command = require(`../commands/${file}`);
    client.commands.set(command.name, command);
    if (!command.hidden && command.module != undefined) {
      client.modules[command.module] = client.modules[command.module]
        ? client.modules[command.module]
        : [];
      client.modules[command.module].push(command);
    }
  }
};