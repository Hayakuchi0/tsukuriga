const path = require('path')
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const glob = require('glob')

let entries = {}
glob.sync('./assets/src/*.js').map(file => {
  const filename = path.basename(file).split('.')[0]
  entries['js/' + filename] = file
})

module.exports = {
  context: __dirname,
  entry: entries,
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
    new ExtractTextPlugin('css/styles-[hash].css'),
  ]
}
