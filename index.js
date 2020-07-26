const fs = require('fs');
const Discord = require('discord.js');
const { token } = require('./config.json');
const isAsync = (f) => f.constructor.name === 'AsyncFunction';
const chalk = require('chalk');
const processCommand = require('./utils/processCommand');

console.log(fs.readFileSync('./assets/banner.txt').toString() + '\n');

const oldLog = console.log;
console.log = (msg, primary = true) => {
	fs.appendFileSync(
		`./logs/${new Date().toLocaleDateString().replace(/\//g, '.')}.log`,
		`[Nicory][LOG][${new Date().toLocaleString()}] ${msg}\n`,
	);
	if (primary) {
		oldLog(
			`[${chalk.magenta('Nicory')}][${chalk.yellowBright(
				'LOG',
			)}][${new Date().toLocaleString()}] ${msg}`,
		);
	}
};

const client = new Discord.Client({ fetchAllMembers: true });
client.commands = new Discord.Collection();
client.modules = {};

const commandFiles = fs
	.readdirSync('./commands')
	.filter((file) => file.endsWith('.js') || file.endsWith('.js'));

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

client.once('ready', () => {
	console.log(`Logged in to Discord as ${client.user.tag}`);
});

client.on('message', async (message) => {
	await processCommand(message, client);
});

client.on('messageUpdate', async (oldMsg, newMsg) => {
	await processCommand(newMsg, client);
});

require('./events/expEvent.js')(client);
require('./events/onJoin')(client);

client.login(token);

module.exports = client;

const Backend = require('./backend/index.js');
new Backend(client);
