from telethon import events, TelegramClient
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.sessions import StringSession
import asyncio
import os
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session = os.getenv("SESSION")
OWNER_ID = 8695947788

bot = TelegramClient(StringSession(session), api_id, api_hash)
async def is_admin(event):
    perms = await bot.get_permissions(event.chat_id, event.sender_id)
    return perms.is_admin

@bot.on(events.NewMessage(pattern=r"\.ban"))
async def ban_user(event):
    if not await is_admin(event):
        return

    if not event.is_group:
        return

    reply = await event.get_reply_message()
    if not reply:
        await event.reply('ᴿᵉᵖˡʸ ᵗᵒ ᵃ ᵘˢᵉʳ ᵗᵒ ᵇᵃⁿ')
        return

    user = reply.sender_id
    ban_rights = ChatBannedRights(until_date=None, view_messages=True)

    await bot(EditBannedRequest(
        event.chat_id,
        user,
        ban_rights
    ))
    await event.reply('ᵁˢᵉʳ ᴮᵃⁿⁿᵉᵈ!')

@bot.on(events.NewMessage(pattern=r"\.unban"))
async def un_ban_user(event):
    if not await is_admin(event):
        return
    if not event.is_group:
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply('ᴿᵉᵖˡʸ ᵗᵒ ᵃ ᵘˢᵉʳ ᵗᵒ ᵁⁿᴮᵃⁿ')
        return
    user = reply.sender_id
    unban_rights = ChatBannedRights(
        until_date=None,
        view_messages=False,
        send_messages=False,
        send_media=False,
        send_gifs=False,
        send_stickers=False,
        embed_links=False,
    )
    await bot(EditBannedRequest(
        event.chat_id,
        user,
        unban_rights
    ))
    await event.reply('ᵁˢᵉʳ ᵁⁿᴮᵃⁿⁿᵉᵈ!')

@bot.on(events.NewMessage(pattern=r"\.unmute"))
async def unmute_user(event):
    if not await is_admin(event):
        return
    if not event.is_group:
        return

    reply = await event.get_reply_message()
    if not reply:
        await event.reply('ᴿᵉᵖˡʸ ᵗᵒ ᵃ ᵘˢᵉʳ ᵗᵒ ᵁⁿᴹᵘᵗᵉ')
        return

    user = reply.sender_id
    unmute_rights = ChatBannedRights(
        until_date=None,
        view_messages=False,
        send_messages=False,
        send_media=False,
        send_gifs=False,
        send_stickers=False,
        embed_links=False

    )

    await bot(EditBannedRequest(
        event.chat_id,
        user,
        unmute_rights
    ))
    await event.reply('ᶠⁱⁿᵉ ᵗʰᵉʸ ᶜᵃⁿ ˢᵖᵉᵃᵏ ᵃᵍᵃⁱⁿ!')

@bot.on(events.NewMessage(pattern=r"\.mute"))
async def mute_user(event):
    if not await is_admin(event):
        return
    if not event.is_group:
        return

    reply = await event.get_reply_message()
    if not reply:
        await event.reply('ᴿᵉᵖˡʸ ᵗᵒ ᵃ ᵘˢᵉʳ ᵗᵒ ᵐᵘᵗᵉ')
        return
    user = reply.sender_id
    mute_rights = ChatBannedRights(
        until_date=None,
        send_messages=True
    )
    await bot(EditBannedRequest(
        event.chat_id,
        user,
        mute_rights
    ))
    await event.reply('ᵁˢᵉʳ ᶠʳᵒᶻᵉⁿ. ᴺᵒ ᵐᵉˢˢᵃᵍᵉˢ ᵃˡˡᵒʷᵉᵈ')

@bot.on(events.NewMessage(pattern=r"\.spam (\d+) (.+)"))
async def spam(event):
    if event.sender_id != OWNER_ID:
        return
    count = int(event.pattern_match.group(1))
    message = event.pattern_match.group(2)
    await event.reply(f"ˢᵖᵃᵐᵐⁱⁿᵍ {count} ᵐᵉˢˢᵃᵍᵉˢ..")
    if count > 20:
        return await event.reply("ᴸⁱᵐⁱᵗ ⁱˢ ²⁰")
    for _ in range(count):
        await event.respond(message)
        await asyncio.sleep(1)
    await event.reply('ˢᵖᵃᵐ ᶜᵒᵐᵖˡᵗᵉᵈ..!')

@bot.on(events.NewMessage(pattern=r"\.dmspam (\d+) (.+)"))
async def dm_spam(event):
    if  event.sender_id != OWNER_ID:
        return
    reply = await event.get_reply_message()
    if not reply:
        await event.reply('ᴿᵉᵖˡʸ ᵗᵒ ᵃ ᵐᵉˢˢᵃᵍᵉ ᵗᵒ ᴰᴹˢᵖᵃᵐ...')
        return
    user = reply.sender_id
    count = int(event.pattern_match.group(1))
    message = event.pattern_match.group(2)
    await event.reply(f'ˢᵖᵃᵐᵐⁱⁿᵍ {count} ᵐᵉˢˢᵃᵍᵉˢ..')
    if count > 20:
        return await event.reply("ᴸⁱᵐⁱᵗ ⁱˢ ²⁰")
    for _ in range(count):
        await event.send_message(user, message)
        await asyncio.sleep(2)
    await event.reply('ᴰᴹˢᵖᵃᵐ ᶜᵒᵐᵖˡᵉᵗᵉᵈ..')

async def main():
    await bot.connect()
    print('Bot is running...')
    await bot.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
