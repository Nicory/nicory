const client = require("../");
const config = require("../config.json");

module.exports = async fastify => { 
  fastify.get("/commands", async (req, res) => { 
    return client.modules;
  });
  
  fastify.get("/stats", async (req, res) => { 
    return {
      prefix: config.prefix,
      guilds: client.guilds.cache.size,
      users: client.users.cache.size,
      channels: client.channels.cache.size
    }
  });
};