from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler

# Botones que aparecen debajo del chat
MAIN_MENU = ReplyKeyboardMarkup(
    [["/5", "/15", "/25"], ["/ayuda"]],
    resize_keyboard=True,
)

WELCOME_TEXT = (
    "¡Hola! Soy tu temporizador Pomodoro 🍅\n\n"
    "Elige /5, /15 o /25 para iniciar un temporizador.\n"
    "Usa /ayuda para ver todos los comandos."
)

HELP_TEXT = (
    "🍅 Comandos Pomodoro\n\n"
    "/5 — inicia 5 minutos de enfoque\n"
    "/15 — inicia 15 minutos de enfoque\n"
    "/25 — inicia un Pomodoro de 25 minutos\n"
    "/ayuda — muestra esta ayuda"
)


async def start_command(update, context):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=MAIN_MENU)


async def help_command(update, context):
    await update.message.reply_text(HELP_TEXT, reply_markup=MAIN_MENU)


def register_command_handlers(application):
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler(["ayuda", "help"], help_command))
