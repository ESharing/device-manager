const fs = require("fs");
const path = require("path");
const Mock = require("mockjs");
const JSON5 = require("json5");
 
function getJsonFile(filePath) {
  var json = fs.readFileSync(path.resolve(__dirname, filePath), "utf8");
  return JSON5.parse(json);
}
 
module.exports = function(app) {
  app.get("/yang-schemas/1.1.1.1", function(req, res) {
    var json = getJsonFile("./schemas.json5");
    res.json(Mock.mock(json));
  });
  app.get("/objects/1.1.1.1", function(req, res) {
    var json = getJsonFile("./objects.json5");
    res.json(Mock.mock(json));
  });
};