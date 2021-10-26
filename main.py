# (c) @AbirHasan2005

import os
import asyncio
import traceback
from dotenv import (
    load_dotenv
)
from pyrogram import (
    Client,
    filters,
    idle
)
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.errors import (
    MessageNotModified
)
from core.search_video import search_pdisk_videos

if os.path.exists("configs.env"):
    load_dotenv("configs.env")


class Configs(object):
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    PDISK_USERNAME = os.environ.get("PDISK_USERNAME", "")
    PDISK_PASSWORD = os.environ.get("PDISK_PASSWORD", "")
    MAX_RESULTS = int(os.environ.get("MAX_RESULTS", 5))
    # Which PDisk Domain?
    PDISK_DOMAINS = [
        "https://www.cofilink.com/",
        "https://www.pdisk1.net/",
        "https://www.pdisk.net/"
    ]
    PDISK_DOMAIN = os.environ.get("PDISK_DOMAIN", PDISK_DOMAINS[2])


PDiskBot = Client(
    session_name=":memory:",
    api_id=Configs.API_ID,
    api_hash=Configs.API_HASH,
    bot_token=Configs.BOT_TOKEN
)



@PDiskBot.on_message(filters.command("start") & ~filters.edited)

async def start_handler(_, m: Message):
    await m.reply_video("https://telegra.ph/file/76045a4ef3f8cdb2ba153.mp4",
        caption="**Watch Above Tutorial 👆**\n\nExamples-\n`@PlayitlinkBot See S02E01`\n`@PlayitlinkBot doctor 2021`",
        reply_markup=InlineKeyboardMarkup([
                           [InlineKeyboardButton("🔍 SEARCH 🔎", switch_inline_query_current_chat="")],
                           [InlineKeyboardButton("⭐RATE ME ⭐", url="https://t.me/tlgrmcbot?start=playitlinkbot-bot")]
                       ]))


    


@PDiskBot.on_message(filters.command("PlayitlinkBot", prefixes=["@", "/"]) & ~filters.edited, group=-1)
async def text_handler(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("Search Query Missing!")
    editable = await m.reply_text("Cooking your results\nPlease Wait...\n\n🔥 Join For Movies @netflixorgi\n🔥 Join For Series @malayayalies", quote=True)
    response = await search_pdisk_videos(m.text.split(" ", 1)[-1], Configs.PDISK_USERNAME, Configs.PDISK_PASSWORD)
    if isinstance(response, Exception):
        traceback.print_exc()
        try: await editable.edit("Failed to search!",
                                 reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton("Support Group", url="https://t.me/malayayalies")]
                                 ]))
        except MessageNotModified: pass
    elif not response["data"]["list"]:
        try: await editable.edit(f"Oops! Query Not Found!\n**Note:- Before Requesting Check Your Spelling** ",
                                 reply_markup=InlineKeyboardMarkup([
                           [InlineKeyboardButton("Request Here 🔰", url="https://t.me/Netflixcontacttbot")]
                       ]))
        except MessageNotModified: pass
    else:
        data = response["data"]["list"]
        text = ""
        count = 0
        for i in range(len(data)):
            if count > Configs.MAX_RESULTS:
                break
            count += 1
            text += f" **{data[i]['title']}**\n" \
                    f"**PDisk Link:** {Configs.PDISK_DOMAIN + 'share-video?videoid=' + data[i]['share_link'].split('=', 1)[-1]}\n\n"
        try: await editable.edit(text, disable_web_page_preview=True)
        except MessageNotModified: pass


async def run():
    await PDiskBot.start()
    print("\n\nBot Started!\n\n")
    await idle()
    await PDiskBot.stop()
    print("\n\nBot Stopped!\n\n")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
