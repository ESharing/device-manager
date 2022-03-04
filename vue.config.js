const path = require("path");
const mock = require('./mock/index.js')
function resolve(dir) {
  return path.join(__dirname, dir);
}

module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    before: function (app, server) {
      mock(app)
    },
    proxy: {  //配置跨域
      '/api': {
        target: 'http://localhost:8081/',  //后台地址
        changOrigin: true,  //允许跨域
        pathRewrite: {
          '^/api': ''
        }
      },
    },
  },
  configureWebpack: {
    devtool: 'source-map'
  },
  chainWebpack: config => {
    config.resolve.alias
      .set("@", resolve("src"))
      .set("assets", resolve("src/assets"))
      .set("components", resolve("src/components"))
      .set("base", resolve("baseConfig"))
      .set("public", resolve("public"));
  },
}
