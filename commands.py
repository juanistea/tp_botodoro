from telegram.ext import CommandHandler

WELCOME_TEXT = (
    "¡Hola! Soy tu temporizador Pomodoro 🍅\n\n"
    "Elige /5, /15 o /25 para iniciar un temporizador."
)


async def start_command(update, context):
    await update.message.reply_text(WELCOME_TEXT)


def register_command_handlers(application):
    application.add_handler(CommandHandler("start", start_command))
