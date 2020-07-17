NodeCache = require 'node-cache'

class Cache
  constructor: (@ttl) ->
    @cache = new NodeCache {stdTtl: @ttl, checkPeriod: @ttl * .2}

  get(key, storeFunc) ->
    value = @cache.get key

    if !value
      value = await storeFunc()
      @cache.set(key, value)

    return value

  del(key) ->
    @cache.del key

  