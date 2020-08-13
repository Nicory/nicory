const express = require("express");
const client = require("../");
const config = require("../config.json");
const db = require("../utils/database.js");

const publc = express.Router();
publc.get("/commands", (req, res) => {
  res.json(client.modules);
});

publc.get("/stats", (req, res) => {
  res.json({
    prefix: config.prefix,
    guilds: client.guilds.cache.size,
    channels: client.channels.cache.size,
    users: client.users.cache.size,
  });
});

publc.get("/auth/:token", async (req, res) => {
  const guildId = await db.get(req.params.token, "token", undefined);
  console.log(guildId);
  if (!guildId) return res.status(401).end();
  const guild = client.guilds.cache.get(guildId);
  const roles = {};
  const channels = {};
  for (const role of guild.roles.cache) {
    if (role[1].position >= guild.members.cache.get(client.user.id).roles.highest.position) {
      roles[role[1].name] = { id: role[1].id, managable: false };
      continue;
    }
    roles[role[1].name] = { id: role[1].id, managable: true };
  }
  for (const channel of guild.channels.cache.array(e => e)) {
    channels[channel.name] = { id: channel.id, type: channel.type };
  }
  if (!guild) return res.status(401).end();
  res
    .json({
      icon: guild.iconURL(),
      name: guild.name,
      roles,
      channels,
    })
    .end();
});

module.exports = publc;
