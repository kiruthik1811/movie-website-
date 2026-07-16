const express = require('express');
const router = express.Router();
const movies = require('../data/movies.json');

// GET all movies
router.get('/', (req, res) => {
  const { phase } = req.query;
  let result = [...movies];

  if (phase) {
    result = result.filter(m => m.phase === parseInt(phase));
  }

  res.json({ success: true, count: result.length, data: result });
});

// GET single movie by ID
router.get('/:id', (req, res) => {
  const movie = movies.find(m => m.id === parseInt(req.params.id));
  if (!movie) {
    return res.status(404).json({ success: false, message: 'Movie not found' });
  }
  res.json({ success: true, data: movie });
});

module.exports = router;
