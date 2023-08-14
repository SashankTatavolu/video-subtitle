const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
module.exports = {
  // ...other config options...

  // Set the CSP options
  chainWebpack: (config) => {
    config.plugin('html').tap((args) => {
      args[0].meta = {
        'http-equiv': 'Content-Security-Policy',
        content: 'default-src \'self\' http://localhost:8080 http://localhost:5000',
      };
      return args;
    });
  },
};