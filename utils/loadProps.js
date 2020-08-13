const fs = require("fs");
const path = require("path");

module.exports = (dir = path.join(process.cwd(), "assets", "properties")) => {
  const content = fs.readdirSync(dir);
  const props = {};
  for(const filePath of content) {
    const json = JSON.parse(fs.readFileSync(path.join(dir, filePath), "utf-8"));
    if(!json._namespace) {
      throw new Error("Wrong schema");
    }
    props[json._namespace] = Object.assign(json, {_namespace: undefined}, props[json._namespace] ?? {});
  }
  return props;
};