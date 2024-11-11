const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Serve static files (sender.html, receiver.html)
app.use(express.static('public'));

let receiverSocket = null;

io.on('connection', (socket) => {
  console.log('A user connected: ' + socket.id);

  // When a receiver is ready, store their socket id
  socket.on('receiverReady', () => {
    console.log('Receiver ready:', socket.id);
    receiverSocket = socket;
  });

  // When sender tries to connect, check if a receiver is available
  socket.on('offer', (data) => {
    console.log('Offer received from sender');
    if (receiverSocket) {
      receiverSocket.emit('offer', data);  // Send offer to receiver
    } else {
      socket.emit('noReceiver');  // Notify sender if no receiver is online
    }
  });

  // When receiver sends an answer, forward it to the sender
  socket.on('answer', (data) => {
    console.log('Answer received from receiver');
    socket.emit('answer', data);
  });

  // Forward ICE candidates between sender and receiver
  socket.on('candidate', (data) => {
    console.log('ICE candidate received');
    if (receiverSocket) {
      receiverSocket.emit('candidate', data);  // Forward to receiver
    }
  });

  // Handle disconnections
  socket.on('disconnect', () => {
    console.log('A user disconnected: ' + socket.id);
    if (socket === receiverSocket) {
      receiverSocket = null;  // Clear receiver socket when they disconnect
    }
  });
});

// Start the server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});