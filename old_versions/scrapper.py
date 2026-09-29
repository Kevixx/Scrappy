

from telethon import TelegramClient

from dotenv import load_dotenv
import os

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
channel_name = "Test Marketplace"

keywords = ["snuff", "puff", "nicotine", "vape"]

# Use a new session name to avoid "database locked" errors
client = TelegramClient('session_terminal', api_id, api_hash)

async def main():
    print("1. Connecting to Telegram servers...")
    await client.connect()

    # Check if you are already authorized. If not, it asks for the code.
    if not await client.is_user_authorized():
        print("2. ⚠️ LOGIN REQUIRED! Check for an input box below this cell.")
        await client.send_code_request(phone_number)
        code = input('Enter the code you received on Telegram: ')
        await client.sign_in(phone_number, code)
        
    print("3. Login successful! Starting scan...")

    found_count = 0
    try:
        # Iterate through history
        async for message in client.iter_messages(channel_name, limit=100):
            if message.text:
                text = message.text.lower()
                for word in keywords:
                    if word in text:
                        print(f"⚠️ MATCH: {word.upper()} | User: {message.sender_id}")
                        print(f"   Msg: {message.text[:50]}...")
                        found_count += 1
                        break 
    except ValueError:
        print(f"❌ ERROR: Could not find the channel '{channel_name}'. Check the spelling!")
    except Exception as e:
        print(f"❌ ERROR: {e}")

    print(f"4. ✅ Scan finished. Found {found_count} messages.")
    await client.disconnect()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
