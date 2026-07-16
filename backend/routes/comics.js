const express = require('express');
const router = express.Router();
const comics = require('../data/comics.json');

// GET all comics
router.get('/', (req, res) => {
  res.json({ success: true, count: comics.length, data: comics });
});

// GET single comic by ID
router.get('/:id', (req, res) => {
  const comic = comics.find(c => c.id === parseInt(req.params.id));
  if (!comic) {
    return res.status(404).json({ success: false, message: 'Comic not found' });
  }
  res.json({ success: true, data: comic });
});

module.exports = router;
