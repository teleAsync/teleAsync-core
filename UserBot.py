
from telethon import events, TelegramClient

@client.on(events.NewMessage(pattern=r"\.info(?: |$)(.*)"))
async def info(event):
    user_input = event.pattern_match.group(1)

    # Get target user
    if user_input:
        user = await client.get_entity(user_input)
    elif event.reply_to_msg_id:
        reply = await event.get_reply_message()
        user = await reply.get_sender()
    else:
        user = await event.get_sender()

    # Extract details
    first_name = user.first_name or "N/A"
    last_name = user.last_name or ""
    username = f"@{user.username}" if user.username else "No username"
    user_id = user.id

    # Send result
    await event.reply(
        f"👤 **User Info**\n\n"
        f"• Name: {first_name} {last_name}\n"
        f"• Username: {username}\n"
        f"• ID: `{user_id}`"
    )
@client.on(events.NewMessage(pattern=r"\.spam (\d+) (.+)"))
async def spam(event):
    count = int(event.pattern_match.group(1))
    message = event.pattern_match.group(2)

    if count > 50:
        return await event.reply("❌ Limit is 50 messages (safety)")

    await event.delete()

    for i in range(count):
        await event.respond(message)
        await asyncio.sleep(0.5) 
@client.on(events.NewMessage(pattern=r"\.tagall(?: |$)(.*)"))
async def tagall(event):
    msg = event.pattern_match.group(1) or "Hello everyone!"
    chat = await event.get_chat()

    await event.reply("📣 Starting mentions (rate-limited)…")

    count = 0
    async for user in client.iter_participants(chat):
        if user.bot or user.deleted:
            continue

        try:
            mention = f"[{user.first_name}](tg://user?id={user.id})"
            await event.respond(f"{mention} {msg}")
            count += 1
            await asyncio.sleep(1.2)  # keep it safe
        except Exception:
            await asyncio.sleep(2)

        if count >= 30:  # hard cap per run
            break

    await event.respond("✅ Done.")

print("🚀 Userbot Running...")
client.start()
client.run_until_disconnected()