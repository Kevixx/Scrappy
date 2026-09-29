from telethon import TelegramClient

import asyncio

from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = TelegramClient('session_terminal_v1', api_id, api_hash)

async def main():
    await client.start()
    
    print("📋 Listing all chats your account is in...")
    print("-" * 30)
    
    # Iterate through all your dialogs (chats/channels)
    async for dialog in client.iter_dialogs():
        # Print the Name and the ID
        print(f"Name: {dialog.name}")
        print(f"ID:   {dialog.id}")
        print("-" * 30)

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
