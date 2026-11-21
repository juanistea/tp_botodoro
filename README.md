# Bot Pomodoro para Telegram

Bot de Telegram para iniciar, cancelar y consultar temporizadores Pomodoro. Está hecho en Python con la librería `python-telegram-bot`.

## Comandos

| Comando | Acción |
| --- | --- |
| `/start` | Saluda y muestra el menú de botones. |
| `/5` | Inicia un temporizador de 5 minutos. |
| `/15` | Inicia un temporizador de 15 minutos. |
| `/25` | Inicia un Pomodoro de 25 minutos. |
| `/cancel` | Cancela el temporizador activo. |
| `/stats` | Muestra tus estadísticas. |
| `/ayuda` | Muestra los comandos (`/help` también funciona). |

Cada persona puede tener un temporizador activo por chat. Solo se cuentan en las estadísticas los temporizadores que terminan; si se cancela, no se registra. Un bloque de 25 minutos cuenta como Pomodoro.

## Archivos

```text
main.py       # Arranca el bot
commands.py   # /start, /ayuda y /stats
timers.py     # /5, /15, /25 y /cancel
stats.py      # Guarda y lee las estadísticas en data/stats.csv
```

## Cómo ejecutarlo

Se necesita Python 3.12 o superior y un token creado con [@BotFather](https://t.me/BotFather).

1. Copiar `.env.example` como `.env` y poner el token real en `TELEGRAM_BOT_TOKEN`. El archivo `.env` no se sube al repositorio.
2. Instalar las dependencias y arrancar el bot:

```bash
python -m venv venv
venv\Scripts\activate        # En Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Con Docker

Con el `.env` ya creado:

```bash
docker compose up --build -d
docker compose logs -f bot
docker compose down
```

Las estadísticas quedan guardadas en el volumen `pomodoro-data`.

## Cómo funciona

- `ApplicationBuilder` crea el bot con el token y `run_polling()` empieza a recibir mensajes.
- `CommandHandler` responde a `/start`, `/ayuda`, `/stats` y `/cancel`.
- `/5`, `/15` y `/25` empiezan con un número, así que se reciben con un `MessageHandler` y un filtro `Regex`.
- `JobQueue` programa el aviso para cuando termina el tiempo. No usamos `time.sleep` porque frenaría al bot.
- Los temporizadores activos se guardan en un diccionario en memoria, así que se pierden si se reinicia el bot. Las estadísticas quedan en el CSV.

Más detalle sobre la librería en [`docs/python-telegram-bot.md`](docs/python-telegram-bot.md).
