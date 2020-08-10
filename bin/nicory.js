#!/usr/bin/env node
const child_process = require("child_process");
const fs = require("fs");

require("yargs")
  .usage("nicory <команда>")
  .command("start", "запуск бота", () => {}, () => {
    console.log("Запуск Nicory...");
    child_process.execSync("npm run production");
  })
  .command("stop", "остановка бота", () => {}, () => {
    console.log("Остановка Nicory...");
    child_process.execSync("npm run production:stop");
  })
  .demandCommand(1, '')
  .epilog("Сделано KislBall и EnotKEK3 💜")
  .strict()
  .argv