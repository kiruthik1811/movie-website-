const express = require('express');
const cors = require('cors');
const path = require('path');

const heroesRouter = require('./routes/heroes');
const moviesRouter = require('./routes/movies');
const comicsRouter = require('./routes/comics');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Serve frontend static files
app.use(express.static(path.join(__dirname, '../frontend')));

// API Routes
app.use('/api/heroes', heroesRouter);
app.use('/api/movies', moviesRouter);
app.use('/api/comics', comicsRouter);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Marvel API is running!', timestamp: new Date().toISOString() });
});

// Catch-all: serve frontend index
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`\n🦸 Marvel Website Backend running!`);
  console.log(`🌐 Server: http://localhost:${PORT}`);
  console.log(`📡 API:    http://localhost:${PORT}/api/heroes\n`);
});
