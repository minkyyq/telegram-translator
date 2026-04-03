from pyrogram import Client, filters
from deep_translator import GoogleTranslator
import asyncio

# Данные с my.telegram.org
API_ID = ID 
API_HASH = "HASH"

app = Client("translator", api_id=API_ID, api_hash=API_HASH)

is_active = True
target_lang = "uk" 

@app.on_message(filters.me & filters.command("lang", prefixes="/"))
async def set_language(client, message):
    global target_lang
    if len(message.command) > 1:
        new_lang = message.command[1].lower()
        target_lang = new_lang
    await message.delete()
    
@app.on_message(filters.me & filters.command("off", prefixes="/"))
async def turn_off(client, message):
    global is_active
    is_active = False
    await message.delete()

@app.on_message(filters.me & filters.command("on", prefixes="/"))
async def turn_on(client, message):
    global is_active
    is_active = True
    await message.delete()

@app.on_message(filters.me & filters.text & ~filters.forwarded)
async def translate_everywhere(client, message):
    if not is_active or message.text.startswith("/"):
        return

    original = message.text

    try:
        translated = await asyncio.to_thread(
            GoogleTranslator(source='auto', target=target_lang).translate, 
            original
        )

        if translated and translated.strip().lower() != original.strip().lower():
            await message.edit_text(translated)
            
    except Exception as e:
        print(f"Ошибка перевода: {e}")

if __name__ == "__main__":
    print("бот запущен")
    print(f"Команды: /on, /off, /lang [код_языка]")
    app.run()