module.exports = {
  "env": {
    "node": true,
    "commonjs": true,
    "es2020": true
  },
  "extends": "eslint:recommended",
  "parserOptions": {
    "ecmaVersion": 11
  },
  "rules": {
    "indent": [
      "error",
      2
    ],
    "linebreak-style": [
      "error",
      "unix"
    ],
    "quotes": [
      "error",
      "double"
    ],
    "semi": [
      "error",
      "always"
    ],
    "no-mixed-spaces-and-tabs": [
      "error",
      "smart-tabs"
    ]
  }
};
