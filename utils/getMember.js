module.exports = (arg) => {
  const mentionRegexp = /(<@)?(!)?\d{17,18}(>)?/gm;
  if (!arg.match(mentionRegexp)) return null;
  let id = arg;
  if (arg.startsWith("<@") && arg.endsWith(">")) {
    id = id.slice(2);
    id = id.slice(0, -1);
  }
  if (id.startsWith("!")) {
    id = id.slice(1);
  }
  return id;
};
