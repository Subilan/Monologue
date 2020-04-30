const path = require("path");

module.exports = {
    devServer: {
        proxy: "http://localhost:5000"
    },

    pwa: {
        name: "Monologue",
        themeColor: "#000",
        msTileColor: "#000",
        appleMobileWebAppCapable: 'yes',
        appleMobileWebAppStatusBarStyle: 'black',
        workboxPluginMode: "GenerateSW"
    },

    pluginOptions: {
      'style-resources-loader': {
        preProcessor: 'less',
        patterns: [
          path.resolve(__dirname, "./src/css/*.less")
        ]
      }
    }
}
