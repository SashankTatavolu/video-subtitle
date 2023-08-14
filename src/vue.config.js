// module.exports = {
//     devServer: {
//       proxy: 'http://localhost:5000'
//         }
//   }

// export function chainWebpack(config) {
//   config.plugin('html').tap((args) => {
//     args[0].meta = {
//       'http-equiv': 'Content-Security-Policy',
//       content: 'default-src \'self\' http://localhost:8080 http://localhost:5000',
//     };
//     return args;
//   });
// }  

module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
};
