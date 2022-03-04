const express = require('express')
const fs = require('fs');

const app = express()
const router = express.Router()

// Include controllers
fs.readdirSync("controllers").forEach(function (file) {
  if(file.substr(-3) == '.js') {
    const route = require('./controllers/' + file);
    route.controller(app);
  }
})

router.get('/', function(req, res) {
  res.json({ message: 'API Initialized!'});
});

const port = process.env.API_PORT || 8081;
app.use('/', router);
var server = app.listen(port, function() {
  console.log(`api running on port ${port}`);
});

module.exports = server


