const mongoose = require('mongoose');

const invitationSchema = new mongoose.Schema({
  creator: String,
  movieTitle: String,
  date: String,
  location: String,
  invitees: [String],
  responses: [{
    email: String,
    response: String,
  }],
});

module.exports = mongoose.model('Invitation', invitationSchema);
