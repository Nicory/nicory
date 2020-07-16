express = require "express"
config = require "../config.json"

class Backend
  constructor: (@client) ->
    @app = express()

    @createRoutes()

    @app.listen(config.apiPort, -> console.log "Started server on port #{config.apiPort}")

  createRoutes: ->
    @app.get("/", (req, res) -> res.send("test"))



module.exports = Backend