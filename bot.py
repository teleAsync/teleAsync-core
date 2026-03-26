from telethon import TelegramClient, events
import os

api_id = 37770123
api_hash = 'b99c784ccdfd6873696b6d423e318aca'

client = TelegramClient('session_name', api_id, api_hash)

# Ensure folder exists
os.makedirs("saved_media", exist_ok=True)

@client.on(events.NewMessage)
async def handler(event):
    try:
        message = event.message

        # Better TTL detection
        is_ttl = False

        if getattr(message, "ttl_period", None):
            is_ttl = True

        if message.media and is_ttl:
            print(f"[+] Self-destruct media detected from {event.sender_id}")

            path = await message.download_media(file="saved_media/")
            print(f"[✔] Saved to: {path}")

    except Exception as e:
        print(f"[ERROR] {e}")

print("🚀 Client running...")
client.start()
client.run_until_disconnected()