from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)


def buttons(url: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="🔗 Link 🔗", url=url)],
            [
                InlineKeyboardButton(text="🔄 Refresh 🔄", callback_data="refresh_cat"),
                InlineKeyboardButton(text="🗑️ Close 🗑️", callback_data="close"),
            ],
        ]
    )
    return keyboard


@app.on_message(filters.command("cat") & ~BANNED_USERS)
async def cat(c, m: Message):
    r = await utils.TheApi.request.get("https://api.thecatapi.com/v1/images/search")
    if r.status_code == 200:
        data = r.json()
        cat_url = data[0]["url"]
        if cat_url.endswith(".gif"):
            await m.reply_animation(
                cat_url, caption="meow", reply_markup=buttons(cat_url)
            )
        else:
            await m.reply_photo(cat_url, caption="meow", reply_markup=buttons(cat_url))
    else:
        await m.reply_text("Failed to fetch cat picture 🙀")


@app.on_callback_query(filters.regex("refresh_cat") & ~BANNED_USERS)
async def refresh_cat(c, m: CallbackQuery):
    r = utils.TheApi.request.get("https://api.thecatapi.com/v1/images/search")
    if r.status_code == 200:
        data = r.json()
        cat_url = data[0]["url"]
        if cat_url.endswith(".gif"):
            await m.edit_message_animation(
                cat_url, caption="meow", reply_markup=buttons(cat_url)
            )
        else:
            await m.edit_message_media(
                InputMediaPhoto(media=cat_url, caption="meow"),
                reply_markup=buttons(cat_url),
            )
    else:
        await m.edit_message_text("Failed to refresh cat picture 🙀")
