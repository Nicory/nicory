const getExpForLevel = level => (5*(level*level))+(50*level)+100; // no spaces gang

const getTotalExpForLevel = function(level) {
  let exp = 0;
  let i = 0;

  while (i < level) {
    exp += getExpForLevel(level);
    i++;
  }

  return exp;
};

const getLevelFromExp = function(exp) { 
  let level = 0;
  while (exp >= getExpForLevel(level)) {
    exp -= getExpForLevel(level);
    level++;
  }
  return level;
};

module.exports = { 
  getExpForLevel,
  getTotalExpForLevel,
  getLevelFromExp
};