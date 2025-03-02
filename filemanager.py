import io
import os
import shutil
import time
from os.path import exists, isdir

from pyrogram import filters
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS

MAX_MESSAGE_SIZE_LIMIT = 4090


def humanbytes(size):
    """Convert bytes into a human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


@app.on_message(filters.command("ls") & ~filters.forwarded & ~filters.via_bot & SUDOERS)
@utils.capture_err
async def lst(_, message):
    path = os.getcwd()
    text = message.text.split(" ", 1)
    directory = None

    if len(text) > 1:
        directory = text[1].strip()
        path = directory

    if not exists(path):
        await message.reply(
            text=f"There is no such directory or file with the name `{directory}`. Check again!",
        )
        return

    if isdir(path):
        msg = (
            f"Folders and Files in `{path}`:\n\n"
            if directory
            else "Folders and Files in Current Directory:\n\n"
        )
        files = ""
        folders = ""

        for contents in sorted(os.listdir(path)):
            item_path = os.path.join(path, contents)
            if isdir(item_path):
                folders += f"📁 {contents}\n"
            else:
                size = os.stat(item_path).st_size
                if contents.endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += f"🎵 {contents}\n"
                elif contents.endswith(".opus"):
                    files += f"🎙 {contents}\n"
                elif contents.endswith(
                    (".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")
                ):
                    files += f"🎞 {contents}\n"
                elif contents.endswith(
                    (".zip", ".tar", ".tar.gz", ".rar", ".7z", ".xz")
                ):
                    files += f"🗜 {contents}\n"
                elif contents.endswith(
                    (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ".webp")
                ):
                    files += f"🖼 {contents}\n"
                elif contents.endswith((".exe", ".deb")):
                    files += f"⚙️ {contents}\n"
                elif contents.endswith((".iso", ".img")):
                    files += f"💿 {contents}\n"
                elif contents.endswith((".apk", ".xapk")):
                    files += f"📱 {contents}\n"
                elif contents.endswith(".py"):
                    files += f"🐍 {contents}\n"
                else:
                    files += f"📄 {contents}\n"

        msg += folders + files if files or folders else "__empty path__"
    else:
        size = os.stat(path).st_size
        last_modified = time.ctime(os.path.getmtime(path))
        last_accessed = time.ctime(os.path.getatime(path))

        if path.endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎵"
        elif path.endswith(".opus"):
            mode = "🎙"
        elif path.endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎞"
        elif path.endswith((".zip", ".tar", ".tar.gz", ".rar", ".7z", ".xz")):
            mode = "🗜"
        elif path.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ".webp")):
            mode = "🖼"
        elif path.endswith((".exe", ".deb")):
            mode = "⚙️"
        elif path.endswith((".iso", ".img")):
            mode = "💿"
        elif path.endswith((".apk", ".xapk")):
            mode = "📱"
        elif path.endswith(".py"):
            mode = "🐍"
        else:
            mode = "📄"

        msg = (
            f"<b>Location:</b> {path}\n"
            f"<b>Icon:</b> {mode}\n"
            f"<b>Size:</b> {humanbytes(size)}\n"
            f"<b>Last Modified:</b> {last_modified}\n"
            f"<b>Last Accessed:</b> {last_accessed}\n"
        )

    if len(msg) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "ls.txt"
            await app.send_document(message.chat.id, out_file, caption=path)
            await message.delete()
    else:
        await message.reply(msg)


@app.on_message(filters.command("rm") & ~filters.forwarded & ~filters.via_bot & SUDOERS)
@utils.capture_err
async def rm_files(_, message):
    if len(message.command) < 2:
        return await message.reply("Please provide file(s) or directory(s) to delete.")

    # Split into multiple file names
    files = message.text.split(" ", 1)[1].split()
    deleted_items = []
    errors = []

    for file in files:
        if exists(file):
            if isdir(file):
                try:
                    shutil.rmtree(file)  # Removes a directory and its contents
                    deleted_items.append(f"Directory `{file}`")
                except Exception as e:
                    errors.append(f"Failed to delete directory `{file}`: {str(e)}")
            else:
                try:
                    os.remove(file)  # Removes a file
                    deleted_items.append(f"File `{file}`")
                except Exception as e:
                    errors.append(f"Failed to delete file `{file}`: {str(e)}")
        else:
            errors.append(f"`{file}` doesn't exist!")

    response = ""
    if deleted_items:
        response += "Deleted:\n" + "\n".join(deleted_items) + "\n"
    if errors:
        response += "Errors:\n" + "\n".join(errors)

    await message.reply(response.strip())
