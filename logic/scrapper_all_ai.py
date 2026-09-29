

from telethon import TelegramClient
from dotenv import load_dotenv
import os
import logic.model as model

load_dotenv()

os.makedirs("./evidence", exist_ok=True)

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH') 
phone_number = os.getenv('PHONE_NUMBER')

client = TelegramClient('session_terminal', api_id, api_hash)

async def nicotine_tracer():
    print("1. Connecting to Telegram...")

    await client.start(phone=phone_number)

    me = await client.get_me()
    
    print("✅ Logged in successfully!")
    print("2. fetching all channels...")
    
    total_matches = 0
    
    async for dialog in client.iter_dialogs():
        
        if dialog.is_group or dialog.is_channel:
            print(f"   >> Scanning: {dialog.name}...")
            
            try:
                async for message in client.iter_messages(dialog.id, limit=50):
                    
                    if message.text and message.sender_id != me.id:
                    #if message.text:
                        text = message.text.lower()
                        response = model.test_model_response(text)
                        
                        if response.strip().lower() == "yes":
                            print(f"🚨 MATCH FOUND in '{dialog.name}'!")
                            
                            # 1. Create a unique filename based on channel + message ID
                            # (Sanitize name to remove spaces/illegal chars)
                            safe_name = "".join(x for x in dialog.name if x.isalnum())
                            filename_base = f"./evidence/{safe_name}_msg{message.id}"

                            # # 2. 📸 IF THERE IS A PHOTO/VIDEO: Download it
                            # if message.media:
                            #     path = await message.download_media(file=filename_base)
                            #     print(f"   📸 Saved media evidence to: {path}")

                            # 📝 SAVE THE TEXT LOG
                            with open(f"{filename_base}.txt", "w", encoding="utf-8") as f:
                                f.write(f"CHANNEL NAME: {dialog.name}\n")
                                f.write(f"CHANNEL ID: {dialog.id}\n")
                                f.write(f"SENDER ID: {message.sender_id}\n")
                                f.write(f"DATE: {message.date}\n")
                                username = getattr(dialog.entity, 'username', None)
                                
                                if username:
                                    # CASE A: Public Channel/Group (Easy)
                                    link = f"https://t.me/{username}/{message.id}"
                                    link_type = "Public"
                                    
                                else:
                                    # CASE B: Private Group Logic
                                    raw_id = str(dialog.id)

                                    if raw_id.startswith("-100"):
                                        # ✅ CASE B1: Supergroup/Channel
                                        # These support deep links. We must strip the '-100' prefix.
                                        clean_id = raw_id[4:] 
                                        link = f"https://t.me/c/{clean_id}/{message.id}"
                                        link_type = "Private Supergroup"
                                        
                                    else:
                                        # ❌ CASE B2: Basic Group (ID starts with '-' but not '-100')
                                        # These DO NOT support deep links to specific messages.
                                        link = "Link Unavailable (Basic Group - Upgrade to Supergroup to enable linking)"
                                        link_type = "Basic Group (No Deep Link)"

                                f.write(f"LINK ({link_type}): {link}\n")
                                f.write("-" * 20 + "\n")
                                f.write(message.text)
                                
                            print(f"   📝 Log saved with {link_type} link")

                            total_matches += 1
                        
                        elif response.strip().lower() == "no":
                            pass
                        
                        else:
                            print(f"   Unexpected model response: {response}")
                            print("")

            except Exception as e:
                print(f"   Skipping {dialog.name} (Error: {e})")

    print(f"3. ✅ All channels scanned. Found {total_matches} suspicious messages.")
    await client.disconnect()