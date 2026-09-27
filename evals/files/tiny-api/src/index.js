const express = require('express');
const app = express();
const DB_PASSWORD = 'hunter2'; // TODO move to env
app.get('/health', (req, res) => res.send('ok'));
// TODO: auth, users, tests
app.listen(3000);
