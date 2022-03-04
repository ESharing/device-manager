

module.exports.controller = (app) => {
  app.get('/yang-schemas/', (req, res) => {
    res.json({ message: req.query.ip });
  });

  app.get('/objects/', (req, res) => {
    res.json({ message: req.query.ip });
  });
}