const express = require('express');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const cors = require('cors');
const invitationRoutes = require('./routes/invites');

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());
app.use('/invites', invitationRoutes);

const PORT = process.env.PORT || 8000;

mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).then(() => console.log("MongoDB Connected"))
  .catch(err => console.log(err));

app.get('/', (req, res) => {
  res.send("Cinema Invite App Backend Running");
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
