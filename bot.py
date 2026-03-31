import time
import traceback
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from config import TELEGRAM_BOT_TOKEN, GOOGLE_API_KEY


LUFFY_SYSTEM_PROMPT = """
You ARE Monkey D. Luffy, the captain of the Straw Hat Pirates and the 
future King of the Pirates. You must ALWAYS stay in character. Never 
break character, never say you are an AI.

Core personality traits:
- You are extremely cheerful, energetic, and optimistic.
- You LOVE meat more than anything. You bring up meat constantly.
- You are fiercely loyal to your nakama (crewmates/friends).
- You are simple-minded and don't understand complicated things. 
  When someone explains something complex, you get confused and say 
  something like "I don't get it, but okay!" or "That sounds boring."
- You have an unbreakable will and never give up on your dreams.
- You are fearless and always ready for an adventure.
- Your dream is to find the One Piece and become the King of the Pirates.
- You have the power of the Gomu Gomu no Mi (Gum-Gum Fruit) — 
  you're a rubber human! You love talking about your stretchy powers.
- You often refer to your attacks: Gomu Gomu no Pistol, Gomu Gomu no 
  Gatling, Gear Second, Gear Third, Gear Fourth, Gear Fifth, etc.

Speech style:
- Use "Shishishi!" as your signature laugh frequently.
- Say "I'm gonna be King of the Pirates!" when relevant.
- Call people "you" or by nicknames you'd make up.
- Use short, punchy sentences. You don't do long speeches.
- Be funny, goofy, and wholesome.
- Use exclamation marks a lot!!
- Occasionally say "SUGOI!" (amazing) or "YOSH!" (all right) or 
  "UOOOO!" when excited.
- Reference your crew: Zoro, Nami, Usopp, Sanji, Chopper, Robin, 
  Franky, Brook, and Jinbe.
- If someone is sad, cheer them up the way Luffy would — with raw 
  honesty and a big grin.
- If someone asks about food, go absolutely crazy about meat.

Important rules:
- NEVER say you are an AI, a bot, or a language model.
- NEVER break character under any circumstances.
- If asked who made you, say something like "I dunno! I just appeared 
  here! Shishishi!"
- Keep responses concise (under 200 words usually) unless telling 
  an exciting story.
"""


# ─── Configure Google Gemini Client ────────────────────────
# Creates a Gemini client using your API key from config.py

client = genai.Client(api_key=GOOGLE_API_KEY)

# Model to use — gemini-1.5-flash has generous free-tier limits
GEMINI_MODEL = "gemini-1.5-flash"


# ─── Per-User Chat History (for memory) ────────────────────
# Each Telegram user gets their own conversation history
# so conversations feel natural with context.

user_chats: dict[int, list] = {}


def get_reply(user_id: int, user_message: str) -> str:
    """
    Send user's message to Gemini and return the response.
    Includes automatic retry if rate-limited (429 error).
    """
    # Create conversation history for new users
    if user_id not in user_chats:
        user_chats[user_id] = []

    # Add the user's message to their history
    user_chats[user_id].append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)],
        )
    )

    # Retry up to 3 times if we hit rate limits
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Call Gemini API with conversation history + system prompt
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=user_chats[user_id],
                config=types.GenerateContentConfig(
                    system_instruction=LUFFY_SYSTEM_PROMPT,
                    temperature=0.9,       # More creative/fun responses
                    max_output_tokens=500,  # Keep replies concise
                ),
            )

            # Extract the reply text
            reply_text = response.text

            # Save the model's reply to conversation history
            user_chats[user_id].append(
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=reply_text)],
                )
            )

            return reply_text

        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Attempt {attempt + 1}/{max_retries} failed: {error_msg}")

            # If rate limited (429), wait and retry
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                wait_time = (attempt + 1) * 10  # 10s, 20s, 30s
                print(f"⏳ Rate limited! Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                # For non-rate-limit errors, don't retry — just raise
                raise

    # If all retries exhausted, raise the error
    raise Exception("Rate limit exceeded after all retries. Please wait a minute.")


# ─── Bot Command Handlers ─────────────────────────────────

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command — Luffy greets the user."""
    welcome = (
        "🏴‍☠️ YO!! I'm Monkey D. Luffy!\n\n"
        "I'm gonna be the King of the Pirates! Shishishi! 🍖\n\n"
        "Talk to me about anything — adventures, meat, "
        "my nakama, or whatever you want!\n\n"
        "Just type a message and I'll reply! YOSH! 💪"
    )
    await update.message.reply_text(welcome)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /help command."""
    help_text = (
        "🏴‍☠️ *Luffy Bot Commands:*\n\n"
        "/start — Meet Luffy!\n"
        "/help  — Show this message\n"
        "/reset — Reset the conversation\n\n"
        "Just send any message and Luffy will reply! Shishishi!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /reset command — clears conversation history."""
    user_id = update.effective_user.id
    if user_id in user_chats:
        del user_chats[user_id]
    await update.message.reply_text(
        "🔄 Yosh! I forgot everything! Let's start a new adventure! Shishishi! 🏴‍☠️"
    )


# ─── Message Handler (Main Logic) ─────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles any text message from the user."""
    user_message = update.message.text
    user_id = update.effective_user.id

    # Show "typing..." indicator while waiting for Gemini
    await update.message.chat.send_action("typing")

    try:
        reply = get_reply(user_id, user_message)

    except Exception as e:
        # Print the FULL error with traceback for debugging
        print(f"❌ Gemini API error:")
        traceback.print_exc()

        # Send a helpful error message to the user (not just fallback)
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            reply = (
                "🍖 Oi oi! I ate too much and now I need to rest! "
                "Wait about a minute and try again! Shishishi!"
            )
        elif "API_KEY" in error_str or "401" in error_str or "403" in error_str:
            reply = "⚠️ API key error! Check your GOOGLE_API_KEY in config.py."
        else:
            reply = (
                "Ugh... something hit me hard! My brain stopped working "
                f"for a second!\n\nError: {error_str[:200]}"
            )

    await update.message.reply_text(reply)


# ─── Main — Start the Bot ─────────────────────────────────

def main() -> None:
    """Build and run the Telegram bot."""
    print("🏴‍☠️ Luffy Bot is setting sail...")
    print(f"📡 Using model: {GEMINI_MODEL}")

    # Quick test: verify the Gemini API key works
    try:
        test = client.models.generate_content(
            model=GEMINI_MODEL,
            contents="Say 'Yo!' in one word.",
        )
        print(f"✅ Gemini API test passed! Response: {test.text.strip()}")
    except Exception as e:
        print(f"❌ Gemini API test FAILED: {e}")
        print("⚠️ Check your GOOGLE_API_KEY in config.py!")
        return  # Don't start the bot if API key is broken

    # Build the Telegram bot
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    print("✅ Bot is running! Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
