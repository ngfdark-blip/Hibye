import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

# Logging setup
logging.basicConfig(level=logging.INFO)

# Configuration (Tu dikarî li ser Railway an .env van daneyan veşêrî)
API_ID = int(os.getenv("API_ID", "123456"))  # API ID ya xwe li vir binivîse
API_HASH = os.getenv("API_HASH", "your_api_hash")  # API Hash ya xwe li vir binivîse
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")  # Tokena Botê ya ji BotFather

app = Client("spoof_call_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Menûya سەرەکی و دوگمە
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📞 Call", callback_data="start_call"), InlineKeyboardButton("🎙 My Audio", callback_data="my_audio")],
        [InlineKeyboardButton("📤 Upload Audio", callback_data="upload_audio"), InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_home")]
    ])

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    welcome_text = (
        "**Welcome, Choose an action:**\n\n"
        "Ev bot ji بۆ encamdana پەیوەندیان û birêvebirنا dengî hatiye çêkirin[span_4](start_span)[span_4](end_span)."
    )
    await message.reply_text(welcome_text, reply_markup=main_menu())

@app.on_callback_query()
async def callback_handler(client: Client, callback_query):
    data = callback_query.data
    
    if data == "start_call":
        await callback_query.message.edit_text(
            "📞 **Send the phone number to call:**\n\n"
            "Nimûne: +9647700000000",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_home")]])
        )
    elif data == "back_home":
        await callback_query.message.edit_text(
            "**Welcome, Choose an action:**",
            reply_markup=main_menu()
        )
    elif data == "my_audio":
        await callback_query.answer("Dosyayên dengî yên tomarbûyî[span_5](start_span)[span_5](end_span) ل ڤێرە نیشan didin.", show_alert=True)
    elif data == "upload_audio":
        await callback_query.answer("Fayilekî dengî (.mp3 / .wav) bar bike.", show_alert=True)
    elif data == "admin_panel":
        await callback_query.answer("Admin Panel.", show_alert=True)

# Gava ku bikارهێنەر ژمارەیێ بۆ bot بنێرە بۆ پەیوەندیێ
@app.on_message(filters.text & ~filters.command("start"))
async def handle_phone_number(client: Client, message: Message):
    phone = message.text.strip()
    if phone.startswith("+") or phone.isdigit():
        status_msg = await message.reply_text(
            f"🔄 **Status: Connecting...**\n"
            f"📞 Target: `{phone}`\n"
            f"Live seconds: 0"
        )
        
        # Li vir di cîhana rastîn de API ya calling (wek Twilio an SIP/VoIP) tê girêdan
        # Ji بۆ نموونە ل دووڤ ڤیدیۆیێ[span_6](start_span)[span_6](end_span) لێرە Status دگۆهڕێت بۆ Ringing و پاشان Answered
        
        import asyncio
        await asyncio.sleep(3)
        await status_msg.edit_text(
            f"🔔 **Status: Ringing...**\n"
            f"📞 Target: `{phone}`"
        )
        await asyncio.sleep(3)
        
        # Piştî خەلاسبوونا پەیوەندیێ و tomarbûnê, فایلێ dengî (.mp3 / .wav) tê شاندن[span_7](start_span)[span_7](end_span):
        # await message.reply_audio("path_to_audio.mp3", caption="Call recording: ...")
    else:
        await message.reply_text("❌ Ji kerema xwe re ژمارەیەکا دروست بنێرە.")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
