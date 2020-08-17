const fetch = require("node-fetch");
const config = require("../../config.json");
const Keyv = require("keyv");
const ms = require("ms");

const cache = new Keyv(config.cache, {namespace: "__guildsCountCache"});

module.exports = async () => {
  let result = await cache.get("guilds");
  if(result) return result;
  const resp = await fetch("https://discord.com/api/v6/users/@me/guilds", {
    headers: {
      "Authorization": `Bot ${config.token}`
    }
  });
  const json = await resp.json();
  result = json.length;
  await cache.set("guilds", result, ms("30s"));
  return result;
};