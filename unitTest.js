const assert = require('assert');
const getMember = require('./utils/getMember');
const getChannel = require('./utils/getChannel');
const getRole = require('./utils/getRole');

assert.equal(getMember('<@706600733931339806>'), '706600733931339806', 'should parse discord mention');
assert.equal(
	getMember('<@!706600733931339806>'),
	'706600733931339806',
	'should parse old discord mention',
);
assert.equal(getMember('706600733931339806'), '706600733931339806', 'should just parse id');

assert.equal(getChannel('<#726136778628530227>'), '726136778628530227', 'should parse channel\'s mention');
assert.equal(
	getChannel('726136778628530227'),
	'726136778628530227',
	'should parse channel\'s id',
);

assert.equal(
	getRole('<@&732629414369558618>'),
	'732629414369558618',
	'should parse role\'s mention',
);

assert.equal(
	getRole('732629414369558618'),
	'732629414369558618',
	'should parse role\'s id',
);

console.log('All tests are successful!');