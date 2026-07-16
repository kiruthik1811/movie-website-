const express = require('express');
const router = express.Router();
const heroes = require('../data/heroes.json');

// GET all heroes
router.get('/', (req, res) => {
  const { team, search } = req.query;
  let result = [...heroes];

  if (team) {
    result = result.filter(h => h.team.toLowerCase() === team.toLowerCase());
  }
  if (search) {
    result = result.filter(h =>
      h.name.toLowerCase().includes(search.toLowerCase()) ||
      h.realName.toLowerCase().includes(search.toLowerCase())
    );
  }

  res.json({ success: true, count: result.length, data: result });
});

// GET single hero by ID
router.get('/:id', (req, res) => {
  const hero = heroes.find(h => h.id === parseInt(req.params.id));
  if (!hero) {
    return res.status(404).json({ success: false, message: 'Hero not found' });
  }
  res.json({ success: true, data: hero });
});

module.exports = router;
