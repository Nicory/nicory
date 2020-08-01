const ejs = require("ejs");

module.exports = (tpl, ctx) => {
  return ejs.render(tpl, ctx);
};