from telegram.ext import MessageHandler, filters

# Temporizadores activos.
# La clave es (chat_id, user_id) y el valor es el job programado en JobQueue.
active_timers = {}


def get_key(update):
    return (update.effective_chat.id, update.effective_user.id)


async def start_timer(update, context):
    # El texto llega como "/25" o "/25@nombre_del_bot": nos quedamos con el número
    command = update.message.text.split()[0]
    minutes = int(command.split("@")[0].replace("/", ""))
    key = get_key(update)

    if key in active_timers:
        await update.message.reply_text(
            "Ya tienes un temporizador activo. Espera a que termine."
        )
        return

    # run_once ejecuta timer_finished una sola vez, cuando pasan los segundos indicados
    job = context.job_queue.run_once(timer_finished, minutes * 60, data=(key, minutes))
    active_timers[key] = job

    await update.message.reply_text(
        f"⏱ Temporizador de enfoque de {minutes} minutos iniciado. "
        "¡A concentrarse!"
    )


async def timer_finished(context):
    key, minutes = context.job.data
    chat_id = key[0]

    active_timers.pop(key, None)

    await context.bot.send_message(chat_id=chat_id, text="🔔 ¡Temporizador terminado! Buen trabajo.")


def register_timer_handlers(application):
    # /5, /15 y /25 empiezan con un número, por eso los recibimos como mensajes
    # y usamos una expresión regular para reconocerlos.
    application.add_handler(MessageHandler(filters.Regex(r"^/(5|15|25)\b"), start_timer))
