const express = require("express");
const config = require("../config.json");
const db = require("../utils/database.js");

const router = express.Router();

router.get("/prefix", async (req, res) => {
  const token = req.headers.authorization.split(" ")[1];
  const guildId = await db.get(token, "token", undefined);
  if (!guildId) {
    return res.status(404).end();
  }
  const prefix = await db.get(guildId, "prefix", config.prefix);
  res.send({ prefix }).end();
});

router.post("/prefix", async (req, res) => {
  const token = req.headers.authorization.split(" ")[1];
  const guildId = await db.get(token, "token", undefined);
  if (!guildId) {
    return res.status(404).end();
  }
  if (!req.query.prefix) return res.status(422).end();
  db.set(guildId, "prefix", req.query.prefix).then(() => {
    res.status(201).send({ success: true });
  }).catch(() => {
    res.status(500).send({ success: false });
  });
});

module.exports = router;