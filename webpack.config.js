const path = require('path')
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const glob = require('glob')

function getEntries() {
  let entries = {}
  glob.sync(`./assets/src/*/*.js`).forEach(filepath => {
    const file = filepath.split('/')
    const folder = file.slice(-2, -1)[0]
    const filename = file.slice(-1)[0]
    console.log(filename)
    entries[`${folder}/${filename.split('.')[0]}`] = filepath
  })
  return entries
}

module.exports = {
  context: __dirname,
  entry: getEntries(),
  output: {
    path: path.resolve('./assets/bundles/'),
    filename: '[name]-[hash].js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'babel-loader'
      },
      {
        test: /\.scss$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            'css-loader',
            'sass-loader'
          ]
        })
      }
    ]
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new ExtractTextPlugin('[name]-[hash].css'),
  ]
}
