const express = require("express");
const publc = require("./public");
const config = require("../config.json");
const cors = require('cors');

class Backend { 
  constructor(client) { 
    this.client = client;
    this.app = express();
    this.app.use(cors());
    this.registerRoutes();
    this.app.listen(config.apiPort, () => console.log(`Started server on port ${config.apiPort}`));
  }

  registerRoutes() { 
    this.app.use("/public", publc);
  }
}

module.exports = Backend;