# NicoryBot
config.json:
```json
{
  "token": "token",
  "prefix": "prefix",
  "mongo": "mongo uri"
}
```

**Создание команд**:
```js
// Ебашим файл с любым названием в папке commands
module.exports = {
  name: "название команды",
  hidden: false, // является ли команда скрытой,
  module: "Название модуля, которое будет отображаться в хелпе",
  description: "описание команды",
  aliases: ["алиасы"],
  usage: "использование команды без префикса",
  cooldown: 5, // в секундах
  args: false, // принимает ли команда аргументы
  async execute(message, args){
    // код команды
  },
  permissions: ["массив прав для юзера"]
};
```