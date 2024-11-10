const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS,
  },
});

async function sendInviteEmail(to, movieTitle, date, location) {
  const mailOptions = {
    from: process.env.EMAIL_USER,
    to,
    subject: 'You are invited to watch a movie!',
    text: `Join us for ${movieTitle} on ${date} at ${location}. RSVP now!`,
  };

  await transporter.sendMail(mailOptions);
}

module.exports = sendInviteEmail;
