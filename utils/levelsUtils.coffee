getExpForLevel = (level) -> 5*(level*level)+(50*level)+100; # no spaces gang

getTotalExpForLevel = (level) ->
  exp = 0
  i = 0

  while i < level
    exp += getExpForLevel level
    i++

  return exp

getLevelFromExp = (exp) -> 
  level = 0
  while exp >= getExpForLevel(level)
    exp -= getExpForLevel(level)
    level++
  return level

module.exports = 
  getExpForLevel: getExpForLevel
  getTotalExpForLevel: getTotalExpForLevel
  getLevelFromExp: getLevelFromExp