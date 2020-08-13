module.exports = (commandName, client) => {
  const command =
    client.commands.get(commandName) ||
    client.commands.find(
      (cmd) => cmd.aliases && cmd.aliases.includes(commandName),
    );
  return command;
};