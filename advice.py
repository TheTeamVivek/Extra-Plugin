from pyrogram import filters
from YukkiMusic import app


@app.on_message(filters.command("advice"))
async def advice(_, message):
    A = await message.reply_text("...")
    res = await utils.TheApi.get_advice()
    await A.edit(res)


__MODULE__ = "Aᴅᴠɪᴄᴇ"
__HELP__ = """
/advice - Gᴇᴛ ʀᴀɴᴅᴏᴍ ᴀᴅᴠɪᴄᴇ"""
