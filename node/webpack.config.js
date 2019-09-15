const path = require('path')
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const glob = require('glob')

function getEntries() {
  let entries = {}
  glob.sync(`./src/*/*.js`).forEach(filepath => {
    const file = filepath.split('/')
    const folder = file.slice(-2, -1)[0]
    const filename = file.slice(-1)[0]
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
        test: /\.s?css$/,
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
  watchOptions: {
    poll: 500
  },
  plugins: [
    new BundleTracker({filename: './assets/webpack-stats.json'}),
    new ExtractTextPlugin('[name]-[hash].css'),
  ]
}
