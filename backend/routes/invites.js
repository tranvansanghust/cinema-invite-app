const express = require('express');
const router = express.Router();
const Invitation = require('../models/Invitation');
const sendInviteEmail = require('../utils/mailer');


// Create a new invitation
router.post('/create', async (req, res) => {
  const { creator, movieTitle, date, location, invitees } = req.body;
  try {
    const newInvitation = new Invitation({ creator, movieTitle, date, location, invitees });
    await newInvitation.save();
    res.status(201).json(newInvitation);
  } catch (error) {
    res.status(500).json({ error: "Failed to create invitation" });
  }
});

// Get invitations for a user
router.get('/user/:email', async (req, res) => {
  try {
    const email = req.params.email;
    const invitations = await Invitation.find({ invitees: email });
    res.json(invitations);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch invitations" });
  }
});

router.post('/create', async (req, res) => {
  const { creator, movieTitle, date, location, invitees } = req.body;
  try {
    const newInvitation = new Invitation({ creator, movieTitle, date, location, invitees });
    await newInvitation.save();

    // Send email to invitees
    for (const email of invitees) {
      await sendInviteEmail(email, movieTitle, date, location);
    }

    res.status(201).json(newInvitation);
  } catch (error) {
    res.status(500).json({ error: "Failed to create invitation" });
  }
});


module.exports = router;
