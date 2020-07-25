/*
 * decaffeinate suggestions:
 * DS102: Remove unnecessary code created because of implicit returns
 * Full docs: https://github.com/decaffeinate/decaffeinate/blob/master/docs/suggestions.md
 */
const keyv = require('keyv'); // for caching and stuff
const mongodb = require('mongodb');
const config = require('../config.json');

const cache = {};

module.exports = {
	async get(id, key, def) {
		if (!cache[key]) {
			cache[key] = new keyv(config.cache, { namespace: key });
		}

		const fromCache = await (cache[key].get(`${id}_${key}`));

		if (fromCache) {
			return fromCache;
		}

		const client = await (mongodb.MongoClient.connect(config.mongo));
		const collection = client.db('nicory').collection(key);

		const toBeCached = await (collection.findOne({ id }));
		if (!toBeCached) {
			return def;
		}

		await (cache[key].set(`${id}`, toBeCached.value));

		client.close();

		return toBeCached.value;
	},

	async set(id, key, value) {
		if (!cache[key]) {
			cache[key] = new keyv(config.cache, { namespace: key });
		}

		const client = await (mongodb.MongoClient.connect(config.mongo));
		const collection = client.db('nicory').collection(key);

		collection.updateOne({ id }, { $set: { value } }, { upsert: true });

		client.close();

		return await (cache[key].set(`${id}`, value));
	},

	async delete(id, key) {
		if (!cache[key]) {
			cache[key] = new keyv(config.cache, { namespace: key });
		}

		const client = await (mongodb.MongoClient.connect(config.mongo));
		const collection = client.db('nicory').collection(key);

		collection.deleteMany({ id });

		client.close();

		return await (cache[key].delete(`${id}`));
	},
};
