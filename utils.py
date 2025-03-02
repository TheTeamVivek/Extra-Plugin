import logging
import traceback
from functools import wraps
from traceback import format_exc as err

from config import LOG_GROUP_ID
from pyrogram.errors import ChatWriteForbidden
from pyrogram.types import Message
from TheApi import Client
from YukkiMusic import app
from YukkiMusic.core.mongo import mongodb
from YukkiMusic.misc import SUDOERS

TheApi = Client()
coupledb = {}
greetingsdb = mongodb.greetings

# ----------- Start Of CouplesDb ---------------- #


async def _get_lovers(cid: int):
    chat_data = coupledb.get(cid, {})
    lovers = chat_data.get("couple", {})
    return lovers


async def get_image(cid: int):
    chat_data = coupledb.get(cid, {})
    image = chat_data.get("img", "")
    return image


async def get_couple(cid: int, date: str):
    lovers = await _get_lovers(cid)
    return lovers.get(date, False)


async def save_couple(cid: int, date: str, couple: dict, img: str):
    if cid not in coupledb:
        coupledb[cid] = {"couple": {}, "img": ""}
    coupledb[cid]["couple"][date] = couple
    coupledb[cid]["img"] = img


# ----------- End Of  CouplesDb ---------------- #


# From Now All  below script is taken from https://github.com/TheHamkerCat/WilliamButcherBot
# Please see https://github.com/TheHamkerCat/WilliamButcherBot/blob/dev/LICENSE


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line

    result.append(small_msg)

    return result


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await app.leave_chat(message.chat.id)
            return
        except Exception as err:
            errors = traceback.format_exc()
            error_feedback = split_limits(
                "**ERROR** | {} | {}\n```command\n{}```\n\n```python\n{}```\n".format(
                    0 if not message.from_user else message.from_user.mention,
                    (
                        0
                        if not message.chat
                        else (
                            f"@{message.chat.username}"
                            if message.chat.username
                            else f"`{message.chat.id}`"
                        )
                    ),
                    message.text or message.caption,
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await app.send_message(LOG_GROUP_ID, x)
            raise err

    return capture


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    member = (await app.get_chat_member(chat_id, user_id)).privileges
    if not member:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_video_chats:
        perms.append("can_manage_video_chats")
    return perms


async def authorised(func, subFunc2, client, message, *args, **kwargs):
    chatID = message.chat.id
    try:
        await func(client, message, *args, **kwargs)
    except ChatWriteForbidden:
        await app.leave_chat(chatID)
    except Exception as e:
        logging.exception(e)
        try:
            await message.reply_text(str(e.MESSAGE))
        except AttributeError:
            await message.reply_text(str(e))
        e = err()
        print(str(e))
    return subFunc2


async def unauthorised(
    message: Message, permission, subFunc2, bot_lacking_permission=False
):
    chatID = message.chat.id
    if bot_lacking_permission:
        text = (
            "I don't have the required permission to perform this action."
            + f"\n**Permission:** __{permission}__"
        )
    else:
        text = (
            "You don't have the required permission to perform this action."
            + f"\n**Permission:** __{permission}__"
        )
    try:
        await message.reply_text(text)
    except ChatWriteForbidden:
        await app.leave_chat(chatID)
    return subFunc2


async def bot_permissions(chat_id: int):
    return await member_permissions(chat_id, app.id)


def adminsOnly(permission):
    def subFunc(func):
        @wraps(func)
        async def subFunc2(client, message: Message, *args, **kwargs):
            chatID = message.chat.id

            # Check if the bot has the required permission
            bot_perms = await bot_permissions(chatID)
            if permission not in bot_perms:
                return await unauthorised(
                    message, permission, subFunc2, bot_lacking_permission=True
                )

            if not message.from_user:
                # For anonymous admins
                if message.sender_chat and message.sender_chat.id == message.chat.id:
                    return await authorised(
                        func,
                        subFunc2,
                        client,
                        message,
                        *args,
                        **kwargs,
                    )
                return await unauthorised(message, permission, subFunc2)

            # For admins and sudo users
            userID = message.from_user.id
            permissions = await member_permissions(chatID, userID)
            if userID not in SUDOERS and permission not in permissions:
                return await unauthorised(message, permission, subFunc2)
            return await authorised(func, subFunc2, client, message, *args, **kwargs)

        return subFunc2

    return subFunc


async def set_welcome(chat_id: int, message: str, raw_text: str, file_id: str):
    update_data = {
        "message": message,
        "raw_text": raw_text,
        "file_id": file_id,
        "type": "welcome",
    }

    return await greetingsdb.update_one(
        {"chat_id": chat_id, "type": "welcome"}, {"$set": update_data}, upsert=True
    )


async def set_goodbye(chat_id: int, message: str, raw_text: str, file_id: str):
    update_data = {
        "message": message,
        "raw_text": raw_text,
        "file_id": file_id,
        "type": "goodbye",
    }

    return await greetingsdb.update_one(
        {"chat_id": chat_id, "type": "goodbye"}, {"$set": update_data}, upsert=True
    )


async def get_welcome(chat_id: int) -> (str, str, str):
    data = await greetingsdb.find_one({"chat_id": chat_id, "type": "welcome"})
    if not data:
        return "", "", ""

    message = data.get("message", "")
    raw_text = data.get("raw_text", "")
    file_id = data.get("file_id", "")

    return message, raw_text, file_id


async def del_welcome(chat_id: int):
    return await greetingsdb.delete_one({"chat_id": chat_id, "type": "welcome"})


async def get_goodbye(chat_id: int) -> (str, str, str):
    data = await greetingsdb.find_one({"chat_id": chat_id, "type": "goodbye"})
    if not data:
        return "", "", ""

    message = data.get("message", "")
    raw_text = data.get("raw_text", "")
    file_id = data.get("file_id", "")

    return message, raw_text, file_id


async def del_goodbye(chat_id: int):
    return await greetingsdb.delete_one({"chat_id": chat_id, "type": "goodbye"})


async def set_greetings_on(chat_id: int, type: str) -> bool:
    if type == "welcome":
        type = "welcome_on"
    elif type == "goodbye":
        type = "goodbye_on"

    existing = await greetingsdb.find_one({"chat_id": chat_id})

    if existing and existing.get(type) is True:
        return True

    result = await greetingsdb.update_one(
        {"chat_id": chat_id}, {"$set": {type: True}}, upsert=True
    )

    return result.modified_count > 0 or result.upserted_id is not None


async def is_greetings_on(chat_id: int, type: str) -> bool:
    if type == "welcome":
        type = "welcome_on"
    elif type == "goodbye":
        type = "goodbye_on"

    data = await greetingsdb.find_one({"chat_id": chat_id})
    if not data:
        return False
    return data.get(type, False)


async def set_greetings_off(chat_id: int, type: str) -> bool:
    if type == "welcome":
        type = "welcome_on"
    elif type == "goodbye":
        type = "goodbye_on"

    existing = await greetingsdb.find_one({"chat_id": chat_id})
    if not existing or existing.get(type) is False:
        return True

    result = await greetingsdb.update_one(
        {"chat_id": chat_id}, {"$set": {type: False}}, upsert=True
    )
    return result.modified_count > 0


def extract_urls(reply_markup):
    urls = []
    if reply_markup.inline_keyboard:
        buttons = reply_markup.inline_keyboard
        for i, row in enumerate(buttons):
            for j, button in enumerate(row):
                if button.url:
                    name = (
                        "\n~\nbutton"
                        if i * len(row) + j + 1 == 1
                        else f"button{i * len(row) + j + 1}"
                    )
                    urls.append((f"{name}", button.text, button.url))
