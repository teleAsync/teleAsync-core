import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
import motor.motor_asyncio

load_dotenv()
api_id = os.geten("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

OWNER_ID = 8695947788

mongo = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = mongo.federation

app = Client("ultra_fed", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ---------- Helpers ----------

async def is_fed_admin(user_id):
    data = await db.fed_admins.find_one({"user_id": user_id})
    return True if data else False

async def get_fed_groups():
    groups = []
    async for g in db.fed_groups.find():
        groups.append(g["chat_id"])
    return groups

# ---------- Add Federation Group ----------

@app.on_message(filters.command("joinfed") & filters.group)
async def join_fed(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return
    
    await db.fed_groups.update_one(
        {"chat_id": message.chat.id},
        {"$set": {"chat_id": message.chat.id}},
        upsert=True
    )
    await message.reply("✅ This group joined federation")

# ---------- FBAN ----------

@app.on_message(filters.command("fban"))
async def fban(client, message: Message):

    if not await is_fed_admin(message.from_user.id):
        return

    user_id = None
    reason = "No reason"

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        if len(message.command) > 1:
            reason = " ".join(message.command[1:])
    else:
        if len(message.command) < 2:
            return await message.reply("Usage: /fban user_id reason")
        user_id = int(message.command[1])
        if len(message.command) > 2:
            reason = " ".join(message.command[2:])

    await db.fbans.update_one(
        {"user_id": user_id},
        {"$set": {"reason": reason}},
        upsert=True
    )

    groups = await get_fed_groups()

    banned = 0
    for g in groups:
        try:
            await client.ban_chat_member(g, user_id)
            banned += 1
        except:
            pass

    await message.reply(f"🚫 FBANNED in {banned} groups\nReason: {reason}")

# ---------- FUNBAN ----------

@app.on_message(filters.command("funban"))
async def funban(client, message: Message):

    if not await is_fed_admin(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply("Usage: /funban user_id")

    user_id = int(message.command[1])

    await db.fbans.delete_one({"user_id": user_id})

    groups = await get_fed_groups()

    unbanned = 0
    for g in groups:
        try:
            await client.unban_chat_member(g, user_id)
            unbanned += 1
        except:
            pass

    await message.reply(f"✅ FUNBANNED in {unbanned} groups")

# ---------- Auto Ban on Join ----------

@app.on_message(filters.new_chat_members)
async def auto_fed_ban(client, message: Message):
    for user in message.new_chat_members:
        check = await db.fbans.find_one({"user_id": user.id})
        if check:
            try:
                await client.ban_chat_member(message.chat.id, user.id)
            except:
                pass

# ---------- Add Fed Admin ----------

@app.on_message(filters.command("addfedadmin"))
async def add_admin(client, message: Message):

    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) < 2:
        return

    uid = int(message.command[1])

    await db.fed_admins.update_one(
        {"user_id": uid},
        {"$set": {"user_id": uid}},
        upsert=True
    )

    await message.reply("👑 New Federation Admin Added")

app.run()