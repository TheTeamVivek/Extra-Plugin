import requests
from pyrogram import filters
from YukkiMusic import app


@app.on_message(filters.command("joke"))
async def get_joke(_, message):
    response = requests.get(
        "https://hindi-jokes-api.onrender.com/jokes?api_key=93eeccc9d663115eba73839b3cd9"
    )
    r = response.json()
    joke_text = r["jokeContent"]
    await message.reply_text(joke_text)
