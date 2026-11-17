import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from commands import register_command_handlers


def main():
    # Lee el token desde el archivo .env (o desde las variables de entorno)
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Falta TELEGRAM_BOT_TOKEN. Configúralo en el archivo .env")
        return

    application = ApplicationBuilder().token(token).build()

    register_command_handlers(application)
    register_timer_handlers(application)

    print("Bot iniciado. Presiona Ctrl+C para detenerlo.")
    application.run_polling()


if __name__ == "__main__":
    main()
