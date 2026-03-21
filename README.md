# 🏴‍☠️ Luffy Bot — Telegram Bot

A Telegram bot that talks like **Monkey D. Luffy** from One Piece!  
Powered by **Google Gemini** and built with **python-telegram-bot**.

---

## 📁 Project Structure

```
Luffy Bot/
├── bot.py             # Main bot logic
├── config.py          # API keys go here
├── requirements.txt   # Python dependencies
└── README.md          # You are here!
```

---

## 🚀 Setup Guide

### 1. Get Your API Keys

#### Telegram Bot Token
1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the **bot token** you receive

#### Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy the generated key

### 2. Insert Your Keys

Open `config.py` and replace the placeholder strings:

```python
TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
GOOGLE_API_KEY = "your-google-gemini-api-key"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Bot

```bash
python bot.py
```

You should see:
```
🏴‍☠️ Luffy Bot is setting sail...
✅ Bot is running! Press Ctrl+C to stop.
```

---

## 🤖 Bot Commands

| Command  | Description                  |
|----------|------------------------------|
| `/start` | Luffy greets you!            |
| `/help`  | Shows available commands     |
| `/reset` | Resets conversation history  |

Just send any text message and Luffy will reply!

---

## ✨ Features

- 🧠 **Luffy Personality** — Strong system prompt keeps Luffy in character
- 💬 **Chat Memory** — Each user has their own conversation history
- ⚡ **Async** — Uses modern async/await syntax
- 🔄 **Reset** — Users can clear their history with `/reset`
- 🛡️ **Error Handling** — Graceful error messages if the API fails

---

## 📝 Notes

- The bot uses **Gemini 2.0 Flash** for fast responses
- Chat history is stored **in memory** (resets when the bot restarts)
- You can customize Luffy's personality by editing `LUFFY_SYSTEM_PROMPT` in `bot.py`
