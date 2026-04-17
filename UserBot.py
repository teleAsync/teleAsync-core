import os
import asyncio
from telethon import events,TelegramClient
from dotenv import load_dotenv
from telethon.sessions import StringSession

load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
string = os.getenv("SESSION")
client = TelegramClient(StringSession(string), api_id, api_hash)

@client.on(events.NewMessage(pattern=r"\.whois"))
async def whois(event):
    if event.is_reply:
        user = await (await event.get_reply_message()).get_sender()
    else:
        user = await event.get_sender()

    text = f"""
👤 USER INFO

ID: {user.id}
Name: {user.first_name} {user.last_name}
Username: @{user.username}
Bot: {user.bot}
Verified: {user.verified}
Premium: {getattr(user, 'premium', False)}
"""

    await event.reply(text)

async def main():
    await client.connect()
    print("Bot is running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
