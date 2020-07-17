const path = require("path");
const nodeExternals = require("webpack-node-externals");

module.exports = {
  target: "node",
  entry: "./index.js",
  output: {
    path: path.join(__dirname, "dist"),
    filename: "bundle.js"
  },
  externals: [nodeExternals()],
  module: {
    rules: [{
      test: /\.coffee$/,
      loader: 'coffee-loader'
    }]
  },
};