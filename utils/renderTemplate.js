const Handlebars = require('handlebars');
const helpers = require("handlebars-helpers")([
  "math",
  "string",
  "array",
  "collection",
  "comparison",
  "regex",
  "date",
  "number",
  "object",
  "misc",
  "inflection"
]);

module.exports = (tpl, ctx) => { 
  for (let i = 0; i < Object.keys(helpers).length; i++) { 
    Handlebars.registerHelper(Object.keys(helpers)[i], Object.values(helpers)[i]);
  }
  return Handlebars.compile(tpl)(ctx);
};