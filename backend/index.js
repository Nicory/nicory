const express = require("express");
const publc = require("./public");
const priv = require("./private");
const config = require("../config.json");
const cors = require("cors");
const auth = require("./authMiddleware");

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
    this.app.use("/private", auth, priv);
  }
}

module.exports = Backend;