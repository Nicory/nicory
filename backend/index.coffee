fastify = require "fastify"
config = require "../config.json"

pblc = require "./public.js"

class Backend
  constructor: (@client) ->
    @app = fastify()

    @createRoutes()

    @app.listen(config.apiPort, -> console.log "Started server on port #{config.apiPort}")

  createRoutes: ->
    @app.register(pblc, {prefix: "/public"})



module.exports = Backend