keyv = require "keyv" # for caching and stuff
mongodb = require "mongodb"
config = require "../config.json"

cache = {}

module.exports = 
  get: (id, key, def) ->
    if !cache[key]
      cache[key] = new keyv(config.cache, {namespace: key})
    
    fromCache = await cache[key].get "#{id}_#{key}"

    if fromCache
      return fromCache

    client = await mongodb.MongoClient.connect config.mongo
    collection = client.db('nicory').collection key

    toBeCached = await collection.findOne {id: id}
    if !toBeCached
      return def

    await cache[key].set("#{id}", toBeCached.value)

    client.close()

    return toBeCached.value

  set: (id, key, value) ->
    if !cache[key]
      cache[key] = new keyv(config.cache, {namespace: key})

    client = await mongodb.MongoClient.connect config.mongo
    collection = client.db('nicory').collection key

    collection.updateOne({id: id}, {$set: {value: value}}, {upsert: true})

    client.close()

    await cache[key].set "#{id}", value

  delete: (id, key) ->
    if !cache[key]
      cache[key] = new keyv(config.cache, {namespace: key})

    client = await mongodb.MongoClient.connect config.mongo
    collection = client.db('nicory').collection key

    collection.deleteMany({id: id})

    client.close()

    await cache[key].delete "#{id}"
