from pyrogram import filters
from YukkiMusic import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from TheApi import Wordle

games = {}

@app.on_message(filters.command("wordle"))
async def wordle(client, message):
    chat_id = message.chat.id
    if chat_id in games:
        await message.reply_text(
            "A game is already active in this chat! Finish or end it before starting a new one.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("End Game", callback_data="end_wordle")]])
        )
        return
    
    games[chat_id] = wordle
    result = await wordle.start(chat_id)
    await message.reply_text(
        f"_____\n{result['message']}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Make a Guess", callback_data="make_guess")]])
    )

@app.on_callback_query(filters.regex("make_guess"))
async def make_guess_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    if chat_id not in games:
        await callback_query.answer("Start a game first using /wordle.", show_alert=True)
        return
    
    await callback_query.message.reply_text("Send your 5-letter word guess.")

@app.on_message(filters.command("guess"))
async def make_guess(client, message):
    chat_id = message.chat.id
    if chat_id not in games:
        await message.reply_text("Start a game first using /wordle.")
        return
    
    if len(message.command) < 2:
        await message.reply_text("Please provide a 5-letter word.")
        return
    
    word = message.command[1].lower()
    result = await games[chat_id].guess(chat_id, word)
    hint_message = ""
    if "hint" in result:
        hint_message = f"\nHint: {result['hint']}"
    
    game_state = result.get("game_state", "_____")
    
    await message.reply_text(
        f"{game_state}\n{result.get('message', 'Invalid response.')}{hint_message}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Get Hint", callback_data="get_hint")]])
    )

@app.on_callback_query(filters.regex("get_hint"))
async def get_hint_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    if chat_id not in games:
        await callback_query.answer("Start a game first using /wordle.", show_alert=True)
        return
    
    result = await games[chat_id].hint(chat_id)
    await callback_query.message.reply_text(result["message"])

@app.on_callback_query(filters.regex("end_wordle"))
async def end_game_callback(client, callback_query):
    chat_id = callback_query.message.chat.id
    if chat_id not in games:
        await callback_query.answer("No active game to end.", show_alert=True)
        return
    
    result = await games[chat_id].end(chat_id)
    del games[chat_id]
    await callback_query.message.reply_text(result["message"])