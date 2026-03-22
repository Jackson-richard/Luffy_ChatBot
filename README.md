# 🏴‍☠️ Luffy Telegram Chatbot

A fun and interactive Telegram chatbot that talks like **Monkey D. Luffy** from *One Piece* — energetic, fearless, and always chasing adventure!

---

## 🚀 Features

* 🧠 AI-powered responses using Groq API
* 🏴‍☠️ Luffy-style personality (fun, simple, chaotic energy)
* 💬 Real-time replies on Telegram
* ⚡ Fast responses using LLM models
* 🔄 Supports conversation flow (basic memory)

---

## 🛠️ Tech Stack

* Python 3.10+
* python-telegram-bot (v20+)
* Groq API (Llama models)
* httpx (for API requests)

---

## 📂 Project Structure

```
luffy-bot/
│
├── bot.py          # Main bot logic
├── config.py       # API keys and configuration
├── README.md       # Project documentation
```

---

## 🔑 Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/your-username/luffy-bot.git
cd luffy-bot
```

---

### 2. Install dependencies

```
pip install python-telegram-bot httpx
```

---

### 3. Create `config.py`

Create a file named `config.py` and add:

```
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"

GROQ_API_KEY = "your_groq_api_key_here"

GROQ_MODEL = "llama-3.3-70b-versatile"

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
```

---

### 4. Run the bot

```
python bot.py
```

---

## 🤖 How it Works

1. User sends message on Telegram
2. Bot receives message
3. Message is sent to Groq API
4. AI generates Luffy-style reply
5. Bot sends reply back to user

---

## 🧠 Luffy Personality

The chatbot is designed to:

* Speak in a **simple, energetic tone**
* Love adventure, food, and freedom 🍖
* Be fearless and a little goofy
* Avoid complex explanations
* Stay fully in character

Example:

```
User: I feel tired  
Luffy: Tired ah? 😤 Come on! Let’s eat meat and go on an adventure! Shishishi!
```

---

## 🔒 Notes

* Bot works only while the script is running
* Do not expose your API keys publicly
* Telegram bots are publicly accessible (can be restricted in code)

---

## ⚠️ Troubleshooting

* ❌ `409 Conflict error`
  → Stop multiple running instances of the bot

* ❌ `Model decommissioned`
  → Update `GROQ_MODEL` to latest version

* ❌ No response from bot
  → Check API key and internet connection

---

## 🌟 Future Improvements

* 🧠 Better memory (long conversations)
* 🎙️ Voice replies (Luffy-style)
* ☁️ Cloud deployment (24/7 uptime)
* 🎮 Custom commands (/adventure, /food, etc.)

---

## 🏁 Final Note

This project is for fun and learning.
Not affiliated with *One Piece* officially.

---

**“I’m gonna be King of the Pirates!” 🏴‍☠️**

