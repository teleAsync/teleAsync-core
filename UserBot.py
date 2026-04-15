from telethon import events, TelegramClient
import asyncio


api_id = 37770123
api_hash ="b99c784ccdfd6873696b6d423e318aca"
OWNER_ID = 8695947788

client = TelegramClient("UserBot",api_id,api_hash)

@client.on(events.NewMessage(pattern=r"\.dmspam (\d+) (.+)"))
async def dmspam(event):
    if event.sender_id != OWNER_ID:
        return 

    reply = await event.get_reply_message()

    if not reply:
        await event.reply("Reply to a message to dmspam")
        return
    user = reply.sender_id

    count = int(event.pattern_match.group(1))
    message = event.pattern_match.group(2)

    await event.reply(f"spam {count} messages")
    for _ in range(count):
        await event.send_message(user, message)
        
        await asyncio.sleep(2)

    await event.reply('Done')

@client.on(events.NewMessage(pattern=r"\.spam (\d+) (.+)"))
async def spam(event):
    if event.sender_id !=  OWNER_ID:
        return
    count= int(event.pattern_match.group(1))
    await event.reply('started')
    message= event.pattern_match.group(2)
    for _ in range(count):
        await event.respond(message)
        await asyncio.sleep(2)

async def main():
    await client.start()
    print('Started...')
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())