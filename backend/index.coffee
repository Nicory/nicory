fastify = require "fastify"
config = require "../config.json"

class Backend
  constructor: (@client) ->
    @app = fastify()

    @createRoutes()

    @app.listen(config.apiPort, -> console.log "Started server on port #{config.apiPort}")

  createRoutes: ->
    @app.get("/", (req, res) -> "test")



module.exports = Backend