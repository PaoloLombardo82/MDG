# test_telegram.py - Prueba de envío de mensaje por Telegram

from telegram import Bot
import asyncio
import os
from dotenv import load_dotenv

async def enviar_mensaje():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("❌ Faltan credenciales de Telegram")
        return

    bot = Bot(token=token)
    try:
        await bot.send_message(chat_id=chat_id, text="✅ ¡Prueba exitosa desde tu IA bursátil!")
        print("✅ Mensaje enviado por Telegram")
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")

# Ejecutar la función
asyncio.run(enviar_mensaje())