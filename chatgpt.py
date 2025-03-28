from config import BANNED_USERS
from g4f.client import AsyncClient
from pyrogram import filters
from pyrogram.enums import ParseMode
from YukkiMusic import app

client = AsyncClient()


@app.on_message(filters.command(["ai", "chatgpt", "ask", "gpt4"]) & ~BANNED_USERS)
async def chatgpt_chat(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            "Example:\n\n`/ai write simple website code using html css, js?`"
        )
        return

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])

    x = await message.reply("...")
    model = "gpt-4o-mini" if message.command[0] != "gpt4" else "gpt-4"
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": user_input},
        ],
    )

    response_text = (
        response.choices[0]
        .message.content.replace("[[Login to OpenAI ChatGPT]]()", "")
        .strip()
    )

    # Telegram's max message length is 4096 characters, split if necessary
    if len(response_text) > 4000:
        parts = [
            response_text[i : i + 4000] for i in range(0, len(response_text), 4000)
        ]
        await x.edit(parts[0], parse_mode=ParseMode.DISABLED)
        for part in parts[1:]:
            await message.reply_text(part, parse_mode=ParseMode.DISABLED)
    else:
        await x.edit(response_text, parse_mode=ParseMode.DISABLED)

    await message.stop_propagation()


__MODULE__ = "CʜᴀᴛGᴘᴛ"
__HELP__ = """
/advice - ɢᴇᴛ ʀᴀɴᴅᴏᴍ ᴀᴅᴠɪᴄᴇ ʙʏ ʙᴏᴛ
/ai [ǫᴜᴇʀʏ] - ᴀsᴋ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ ᴡɪᴛʜ ᴄʜᴀᴛɢᴘᴛ's ᴀɪ
/ai [ǫᴜᴇʀʏ] - ᴀsᴋ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ ᴡɪᴛʜ ᴄʜᴀᴛɢᴘᴛ's ᴀɪ Gpt4
/gemini [ǫᴜᴇʀʏ] - ᴀsᴋ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ ᴡɪᴛʜ ɢᴏᴏɢʟᴇ's ɢᴇᴍɪɴɪ ᴀɪ"""
