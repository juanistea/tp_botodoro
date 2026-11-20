# Guía de estudio: `python-telegram-bot`

Este material acompaña a [`presentacion.md`](../presentacion.md) y sirve como apunte para estudiar la librería y preparar el material de entrega.

**Integrantes:** completar con nombres y apellidos.

## 1. Para qué sirve

`python-telegram-bot` es una librería de Python que facilita el uso de la Bot API de Telegram. La librería recibe actualizaciones y ofrece métodos para que nuestro programa responda.

La separación importante es:

- **Telegram** transporta mensajes entre la persona y el bot.
- **`python-telegram-bot`** conecta el programa Python con la Bot API y distribuye actualizaciones.
- **Nuestro programa** decide qué significa cada comando y cómo responder.

## 2. Conceptos básicos

| Nombre | Explicación sencilla |
| --- | --- |
| `Application` | Aplicación que reúne la configuración y los handlers del bot. |
| `Update` | Información sobre algo que pasó en Telegram, como un mensaje nuevo. |
| Handler | Función registrada para atender cierto tipo de actualización. |
| `CommandHandler` | Handler para comandos como `/start` o `/stats`. |
| `MessageHandler` | Handler para mensajes que coinciden con un filtro. |
| Filter | Regla que selecciona qué mensajes procesa un `MessageHandler`. |
| `JobQueue` | Herramienta para programar una función para más adelante. |
| `ReplyKeyboardMarkup` | Teclado de botones que se muestra en el chat. |

## 3. Crear y ejecutar la aplicación

En el proyecto, `main.py` construye la aplicación, registra handlers y empieza el polling:

```python
application = ApplicationBuilder().token(token).build()
register_command_handlers(application)
register_timer_handlers(application)
application.run_polling()
```

El token identifica al bot y debe tratarse como una contraseña. En el proyecto se carga desde el archivo `.env`, no se escribe directamente en el código.

*Polling* significa que la aplicación consulta a Telegram para recibir nuevas actualizaciones. `run_polling()` mantiene ese proceso en marcha.

En `requirements.txt`, la dependencia se escribe como `python-telegram-bot[job-queue]`: el extra `job-queue` instala lo necesario para usar `JobQueue`.

## 4. `CommandHandler`: atender comandos

Un `CommandHandler` asocia un nombre con una función:

```python
application.add_handler(CommandHandler("start", start_command))
```

Cuando la persona manda `/start`, la librería llama a `start_command`. En este proyecto, `commands.py` registra `/start`, `/ayuda`, `/help` y `/stats`.

Los callbacks de handlers se definen como funciones `async`. Para enviar una respuesta se espera la operación con `await`:

```python
async def start_command(update, context):
    await update.message.reply_text("¡Hola!")
```

`update` permite acceder al mensaje que llegó. `context` ofrece recursos disponibles durante su procesamiento.

## 5. `MessageHandler` y filtros

En este bot, `/5`, `/15` y `/25` empiezan con un número. Por eso se registran como mensajes usando una expresión regular:

```python
application.add_handler(MessageHandler(filters.Regex(r"^/(5|15|25)\b"), start_timer))
```

El filtro `Regex` selecciona los mensajes con ese formato. La función `start_timer` obtiene la duración y llama a la lógica del temporizador.

| Situación | Herramienta usada |
| --- | --- |
| `/start` | `CommandHandler` |
| `/stats` | `CommandHandler` |
| `/25` | `MessageHandler` con `filters.Regex` |

## 6. `JobQueue`: ejecutar algo después

Un temporizador necesita avisar en el futuro. `JobQueue.run_once` programa una función para ejecutarse una sola vez:

```python
context.job_queue.run_once(timer_finished, minutes * 60, data=(key, minutes))
```

- `timer_finished` es la función que se llamará.
- `minutes * 60` indica cuánto esperar, en segundos.
- `data` lleva los datos que necesitará esa función.

No se usa `time.sleep`: detenería el programa mientras espera. `JobQueue` deja que el bot continúe procesando otros mensajes.

## 7. `ReplyKeyboardMarkup`: mostrar botones

El proyecto muestra botones para iniciar temporizadores, cancelar y consultar estadísticas:

```python
MAIN_MENU = ReplyKeyboardMarkup(
    [["/5", "/15", "/25"], ["/cancel", "/stats", "/ayuda"]],
    resize_keyboard=True,
)
```

Al tocar un botón, Telegram envía su texto. Por eso el botón `/25` sigue el mismo flujo que escribir `/25` a mano.

## 8. Flujo completo del ejemplo

```text
La persona escribe /5
        ↓
Application recibe un Update
        ↓
MessageHandler + Regex reconoce /5
        ↓
start_timer programa JobQueue
        ↓
JobQueue llama a timer_finished al vencer
        ↓
El bot envía el aviso
```

La librería ofrece los componentes para recibir, seleccionar y programar. La separación multiusuario, el mensaje final y el registro CSV son reglas escritas en este proyecto.

## 9. Componentes del proyecto para mostrar

- `main.py`: crea `Application` y llama a `run_polling()`.
- `commands.py`: usa `CommandHandler` y `ReplyKeyboardMarkup`.
- `timers.py`: usa `MessageHandler`, `filters.Regex`, `JobQueue` y callbacks asíncronos.
- `stats.py`: usa el módulo estándar `csv`; no es una función de Telegram ni de `python-telegram-bot`.

## 10. Referencias

- Documentación oficial de `python-telegram-bot`: <https://docs.python-telegram-bot.org/>
- Telegram Bot API: <https://core.telegram.org/bots/api>
- Código usado como ejemplo: archivos `main.py`, `commands.py` y `timers.py` de este proyecto.
