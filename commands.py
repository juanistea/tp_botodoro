from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler

from stats import get_stats

# Botones que aparecen debajo del chat
MAIN_MENU = ReplyKeyboardMarkup(
    [["/5", "/15", "/25"], ["/cancel", "/stats", "/ayuda"]],
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
    "/cancel — cancela el temporizador activo\n"
    "/stats — muestra tus estadísticas\n"
    "/ayuda — muestra esta ayuda"
)


async def start_command(update, context):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=MAIN_MENU)


async def help_command(update, context):
    await update.message.reply_text(HELP_TEXT, reply_markup=MAIN_MENU)


async def stats_command(update, context):
    stats = get_stats(update.effective_chat.id, update.effective_user.id)
    await update.message.reply_text(
        "📊 Tus estadísticas Pomodoro\n\n"
        f"Hoy: {stats['today_pomodoros']} pomodoros · {stats['today_minutes']} min de enfoque\n"
        f"Total: {stats['total_pomodoros']} pomodoros · {stats['total_minutes']} min de enfoque"
    )


def register_command_handlers(application):
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler(["ayuda", "help"], help_command))
    application.add_handler(CommandHandler("stats", stats_command))
