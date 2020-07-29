const db = require("../utils/database");

module.exports = async (req, res, next) => {
  const auth = req.headers?.authorization?.split(" ");
  if (!auth) { 
    return res.status(401).end();
  }
  if (auth[0] == "Basic") {
    const token = auth[1];
    if (!auth[1]) {
      return res.status(401).end();
    }
    const guildId = await db.get(token, 'token', undefined);
    if (!guildId) { 
      return res.status(401).end();
    }
    next();
  } else { 
    return res.status(401).end();
  }
};