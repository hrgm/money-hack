const path = require('path');
const autoprefixer = require('autoprefixer');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const entry = {};

const variableCostPath = 'variable_cost/static/variable_cost/';

// input
entry[`${variableCostPath}js/input`] = path.resolve(
  __dirname,
  `${variableCostPath}js/input.ts`
);

// list
entry[`${variableCostPath}js/list`] = path.resolve(
  __dirname,
  `${variableCostPath}js/list.ts`
);

module.exports = {
  // モード
  mode: 'development',

  // エントリーポイント
  entry,

  // ファイル出力先
  output: {
    // 出力先ディレクトリ
    path: __dirname,
    // 出力ファイル名
    filename: '[name].bundle.js',
  },

  // ソースマップ
  devtool: 'cheap-module-eval-source-map',

  // ローダー
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              esModule: true,
            },
          },
          {
            loader: 'css-loader',
            options: {
              url: false,
              sourceMap: true,
              importLoaders: 2,
            },
          },
          {
            loader: 'postcss-loader',
            options: {
              plugins: () => [autoprefixer()],
            },
          },
          {
            loader: 'sass-loader',
            options: {
              // Dart Sass を優先
              implementation: require('sass'),
              sassOptions: {
                includePaths: ['./node_modules'],
              },
              sourceMap: true,
              // See https://github.com/webpack-contrib/sass-loader/issues/804
              webpackImporter: false,
            },
          },
        ],
      },
      {
        test: /\.js$/,
        use: [
          {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env'],
            },
          },
        ],
      },
      {
        test: /\.ts$/,
        use: 'ts-loader',
      },
    ],
  },

  // モジュール解決
  resolve: {
    extensions: ['.ts', '.js'],
  },

  // プラグイン
  plugins: [
    new MiniCssExtractPlugin({
      moduleFilename: ({ name }) =>
        `${name.replace('/js/', '/css/')}.bundle.css`,
    }),
  ],
};
