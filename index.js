const fs = require('fs');
const Discord = require('discord.js');
const { prefix, token } = require('./config.json');
const isAsync = (f) => f.constructor.name === "AsyncFunction";
const chalk = require("chalk");

console.log(fs.readFileSync("./assets/banner.txt").toString() + "\n");

const oldLog = console.log;
console.log = (msg, primary = true) => {
  fs.appendFileSync(`./logs/${new Date().toLocaleDateString().replace(/\//g, ".")}.log`, `[Nicory][LOG][${new Date().toLocaleString()}] ${msg}\n`);
  if (primary) { 
    oldLog(
      `[${chalk.magenta("Nicory")}][${chalk.yellowBright(
        "LOG"
      )}][${new Date().toLocaleString()}] ${msg}`
    );
    
  }
}

const client = new Discord.Client();
client.commands = new Discord.Collection();
client.modules = {};

const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js') || file.endsWith('.coffee'));

for (const file of commandFiles) {
  const command = require(`./commands/${file}`);
  client.commands.set(command.name, command);
  if (!command.hidden && command.module != undefined) {
    client.modules[command.module] = client.modules[command.module]
      ? client.modules[command.module]
      : [];
    client.modules[command.module].push(command);
  }
}

const cooldowns = new Discord.Collection();

client.once('ready', () => {
  console.log(`Logged in to Discord as ${client.user.tag}`);
});

client.on('message', async message => {
  if (!message.content.startsWith(prefix) || message.author.bot) return;

  const args = message.content.slice(prefix.length).trim().split(/ +/);
  const commandName = args.shift().toLowerCase();

  const command = client.commands.get(commandName)
    || client.commands.find(cmd => cmd.aliases && cmd.aliases.includes(commandName));

  if (!command) return;

  if (!message.guild) return;

  if (command.args && !args.length) {
    let reply = `Ты привел неверные аргументы, ${message.author}!`;

    if (command.usage) {
      reply += `\nПравильное использование: \`${prefix}${command.name} ${command.usage}\``;
    }

    return message.channel.send(reply);
  }

  if (!cooldowns.has(command.name)) {
    cooldowns.set(command.name, new Discord.Collection());
  }

  const now = Date.now();
  const timestamps = cooldowns.get(command.name);
  const cooldownAmount = (command.cooldown || 1) * 1000;

  if (timestamps.has(message.author.id)) {
    const expirationTime = timestamps.get(message.author.id) + cooldownAmount;

    if (now < expirationTime) {
      const timeLeft = (expirationTime - now) / 1000;
      return message.reply(`подожди еще ${timeLeft.toFixed(1)} секунд перед использование команды \`${command.name}\`!`);
    }
  }

  timestamps.set(message.author.id, now);
  setTimeout(() => timestamps.delete(message.author.id), cooldownAmount);

  if (command.permissions) { 
    let num = 0;
    for (let perm of command.permissions) { 
      num = num | Discord.Permissions.FLAGS[perm];
    }

    if (!message.member.hasPermission(num)) return message.reply("у вас нет прав на запуск этой команды!");
  }


  try {
    await command.execute(message, args, client);
  } catch (error) {
    if (error instanceof Discord.DiscordAPIError) { 
      return message.reply("API ошибка!\nЭто могло произойти по нескольким причинам:\n* У бота нет прав(самое частое)\n* Баги discord.js")
    }
    console.error(error);
    message.reply('произошла ошибка во время запуска команды!');
  }

  console.log(`Executed command ${commandName} by ${message.author.tag}(${message.author.id}) in guild ${message.guild.name}(${message.guild.id}) with following message(${message.id}): ${message.content}`, false);

  
});

require("./events/expEvent.coffee")(client);
require("./events/onJoin")(client);

client.login(token);

const Backend = require("./backend/index.coffee");
new Backend(client);