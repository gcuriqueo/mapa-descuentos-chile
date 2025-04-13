const fs = require('fs')
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,
    host: 'localhost',
    allowedHosts: "all",
    https: {
      key: fs.readFileSync('./localhost+1-key.pem'),
      cert: fs.readFileSync('./localhost+1.pem'),
    },
    headers: {
      'Access-Control-Allow-Origin': 'https://localhost:8080',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'X-XSS-Protection': '1; mode=block',
      'X-Powered-By': ''
    }
  }
})