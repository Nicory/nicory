const fs = require("fs");
const chalk = require("chalk");

module.exports = () => {
  const oldLog = console.log;
  console.log = (msg, primary = true) => {
    fs.appendFileSync(
      `./logs/${new Date().toLocaleDateString().replace(/\//g, ".")}.log`,
      `[Nicory][LOG][${new Date().toLocaleString()}] ${msg}\n`,
    );
    if (primary) {
      oldLog(
        `[${chalk.magenta("Nicory")}][${chalk.blue(
          "LOG",
        )}][${new Date().toLocaleString()}] ${msg}`,
      );
    }
  };
  console.error = (msg, primary = true) => {
    fs.appendFileSync(
      `./logs/${new Date().toLocaleDateString().replace(/\//g, ".")}.log`,
      `[Nicory][ERROR][${new Date().toLocaleString()}] ${msg}\n`,
    );
    if (primary) {
      oldLog(
        `[${chalk.magenta("Nicory")}][${chalk.red(
          "ERROR",
        )}][${new Date().toLocaleString()}] ${msg}`,
      );
    }
  };
  console.warn = (msg, primary = true) => {
    fs.appendFileSync(
      `./logs/${new Date().toLocaleDateString().replace(/\//g, ".")}.log`,
      `[Nicory][WARN][${new Date().toLocaleString()}] ${msg}\n`,
    );
    if (primary) {
      oldLog(
        `[${chalk.magenta("Nicory")}][${chalk.yellow(
          "WARN",
        )}][${new Date().toLocaleString()}] ${msg}`,
      );
    }
  };
};