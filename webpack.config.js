const path = require("path");
const nodeExternals = require("webpack-node-externals");
const webpack = require("webpack");
const package = require('./package.json');

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
  plugins: [
    new webpack.BannerPlugin({
      banner: `NicoryBot v${package.version}-[hash]\nBy: ${package.author}\n`
    })
  ]
};