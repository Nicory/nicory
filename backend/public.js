const express = require("express");
const client = require("../");
const config = require("../config.json");
const db = require('../utils/database.coffee');

const publc = express.Router();
publc.get("/commands", (req, res) => { 
  res.json(client.modules);
});

publc.get("/stats", (req, res) => {
  res.json({
    prefix: config.prefix,
    guilds: client.guilds.cache.size,
    channels: client.channels.cache.size,
    users: client.users.cache.size
  });
});

publc.get("/auth/:token", async (req, res) => {
  const guildId = await db.get(req.params.token, "token", undefined);
  console.log(guildId);
  if (!guildId) return res.status(401).end();
  const guild = client.guilds.cache.get(guildId);
  if (!guild) return res.status(401).end();
  res.json({
    icon: guild.iconURL(),
    name: guild.name
  }).end();
});

module.exports = publc;