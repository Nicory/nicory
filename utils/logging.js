const fs = require('fs');
const chalk = require('chalk');

module.exports = () => {
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
};