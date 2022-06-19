const CompressionWebpackPlugin = require('compression-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

const webpack = require('webpack');
const path = require('path');

const config = {
  mode: 'development',
  entry: {
    app: './src/app.js',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].bundle.js',
    publicPath: '/',
    assetModuleFilename: 'assets/images/[name][ext][query]'
  },
  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          "postcss-loader"
        ]
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
    ]
  },
  devtool: 'inline-source-map',
  plugins: [
    new CleanWebpackPlugin({
      cleanAfterEveryBuildPatterns: ['dist']
    }),
    new CompressionWebpackPlugin({test: /\.js/}),
    new MiniCssExtractPlugin({
      filename: "style.bundle.css",
      ignoreOrder: false,
    }),
    new HtmlWebpackPlugin({
      template: './src/templates/index.html',
      filename: 'index.html'
    }),
    new HtmlWebpackPlugin({
      template: './src/templates/signup.html',
      filename: 'signup.html'
    }),
    new HtmlWebpackPlugin({
      template: './src/templates/login.html',
      filename: 'login.html'
    }),
    new webpack.HotModuleReplacementPlugin()
  ]
};

module.exports = config;