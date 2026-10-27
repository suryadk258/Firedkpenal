
const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json({ limit: "10kb" }));

const PORT = process.env.PORT || 3000;
const BOT_TOKEN = process.env.BOT_TOKEN;

const CHANNELS = [
  "@suryaearningtip",
  "@suryaearningtips",
  "@Jafarearningtrick"
];

app.get("/", (req, res) => {
  res.send("Fire World membership server is running.");
});

app.post("/api/verify", async (req, res) => {
  if (!BOT_TOKEN) {
    return res.status(500).json({
      ok: false,
      message: "Bot token is not configured on the server."
    });
  }

  const userId = Number(req.body.userId);

  if (!Number.isSafeInteger(userId) || userId <= 0) {
    return res.status(400).json({
      ok: false,
      message: "Valid user ID required."
    });
  }

  try {
    const results = await Promise.all(
      CHANNELS.map(async (channel) => {
        const response = await fetch(
          `https://api.telegram.org/bot${BOT_TOKEN}/getChatMember`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              chat_id: channel,
              user_id: userId
            })
          }
        );

        const data = await response.json();

        if (!response.ok || !data.ok) {
          throw new Error("Telegram membership lookup failed.");
        }

        const member = data.result;
        return (
          member.status === "creator" ||
          member.status === "administrator" ||
          member.status === "member" ||
          (member.status === "restricted" &&
            member.is_member === true)
        );
      })
    );

    return res.json({
      ok: true,
      joined: results.every(Boolean),
      channels: results
    });
  } catch (error) {
    console.error("Verification error:", error.message);

    return res.status(502).json({
      ok: false,
      message: "Unable to verify membership. Please try again."
    });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
