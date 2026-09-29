

from telethon import TelegramClient
import asyncio

from dotenv import load_dotenv
import os

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

keywords = ["snuff", "puff", "nicotine", "vape", "snus"]

client = TelegramClient('session_terminal', api_id, api_hash)

async def main():
    print("1. Connecting to Telegram...")

    # 👇 THE FIX: Use start() instead of connect() + return
    # This will connect AND ask for the code if you aren't logged in.
    await client.start(phone=phone_number)
    me = await client.get_me()
    
    print("✅ Logged in successfully!")
    print("2. fetching all channels...")
    
    total_matches = 0
    
    # ... (Rest of your scanning code remains exactly the same) ...
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            print(f"   >> Scanning: {dialog.name}...")
            try:
                async for message in client.iter_messages(dialog.id, limit=50):
                    if message.text and message.sender_id != me.id:
                        text = message.text.lower()
                        for word in keywords:
                            if word in text:
                                print(f"🚨 MATCH FOUND in '{dialog.name}'!")
                                print(f"   Msg: {message.text[:50]}...") 
                                total_matches += 1
            except Exception as e:
                print(f"   Skipping {dialog.name} (Error: {e})")

    print(f"3. ✅ All channels scanned. Found {total_matches} suspicious messages.")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())