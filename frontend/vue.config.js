module.exports = {
  devServer: {
    watchOptions: {
      poll: true
    },
  },
  pages: {
    index: {
      entry: 'src/main.js',
      title: 'KESHIKII',
    }
  },
  outputDir: '../static',
  indexPath: '../templates/index.html',
  publicPath: process.env.NODE_ENV === 'production'
    ? '/static/'
    : '/'
};
