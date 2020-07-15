const assert = require('assert');
const getMember = require("./utils/getMember");

assert.equal(getMember("<@706600733931339806>"), "706600733931339806", "should parse discord mention");
assert.equal(
  getMember("<@!706600733931339806>"),
  "706600733931339806",
  "should parse old discord mention"
);
assert.equal(getMember("706600733931339806"), "706600733931339806", "should just parse id");

console.log("All tests are successful!");