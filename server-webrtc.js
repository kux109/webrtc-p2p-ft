const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static(path.join(__dirname, 'public')));

io.on('connection', (socket) => {
  socket.on('signal', (data) => {
    socket.broadcast.emit('signal', data);
  });
});

server.listen(3000, () => {
  console.log('Server is listening on port 3000');
});