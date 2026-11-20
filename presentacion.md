# Python con Telegram: `python-telegram-bot`

**Duración total:** 20 minutos
**Tema de esta presentación:** la librería `python-telegram-bot` y cómo se usa en el bot Pomodoro.
**Persona 1 (introducción no técnica):** completar nombre y apellido.  
**Persona 2 (explicación técnica y demostración):** completar nombre y apellido.

## Objetivos

Al terminar, la clase debería poder explicar:

1. Qué hace `python-telegram-bot` entre un programa Python y Telegram.
2. Cómo una actualización llega a un handler.
3. La diferencia entre `CommandHandler` y `MessageHandler`.
4. Cómo `JobQueue` programa una acción futura sin bloquear al bot.

Se cubren más de dos componentes funcionales de la librería: `Application`, handlers y filtros, `JobQueue` y `ReplyKeyboardMarkup`.

## Reparto y tiempos

La presentación tiene dos expositores. La Persona 1 realiza una introducción sin tecnicismos; luego la Persona 2 desarrolla la explicación técnica y la demostración. Ambas participan en el cierre y las preguntas.

| Parte | Tiempo | Quién expone |
| --- | ---: | --- |
| Apertura | 1 min | Persona 1: __________ |
| Problema y técnica Pomodoro | 2 min | Persona 1: __________ |
| Qué permite hacer el bot y qué es `python-telegram-bot` | 1 min | Persona 1: __________ |
| Qué hace `python-telegram-bot` y recorrido de una actualización | 2 min | Persona 1: __________ |
| Preparar y ejecutar la aplicación | 1 min | Persona 2: __________ |
| `CommandHandler` | 2 min | Persona 2: __________ |
| `MessageHandler` y filtros | 2 min | Persona 2: __________ |
| `JobQueue` y temporizadores | 3 min | Persona 2: __________ |
| Teclado y estadísticas | 1 min | Persona 2: __________ |
| Demostración del código y funcionamiento | 3 min | Persona 2: __________ |
| Cierre y preguntas | 2 min | Ambas personas: __________ |
| **Total** | **20 min** | |

La Persona 1 no necesita explicar código: presenta el problema, el método Pomodoro, el uso del bot y una explicación general de cómo la librería conecta Telegram con el programa. La Persona 2 toma la palabra después y presenta los componentes técnicos, el código y la demostración.

## Guion por diapositiva

### 1. Apertura — 1 minuto — Persona 1, no técnica

**En pantalla:** título, nombres y un mensaje de Telegram conectado al bot.

> Hoy presentamos nuestro bot Pomodoro para Telegram. Primero vamos a contar qué problema ayuda a resolver y cómo se usa. Después [nombre de Persona 2] mostrará cómo lo construimos y cómo funciona por dentro.

### 2. El problema y la técnica Pomodoro — 2 minutos — Persona 1, no técnica

**En pantalla:** una persona estudiando y un esquema simple de períodos de enfoque y descanso.

> La técnica Pomodoro propone alternar períodos de concentración con descansos. El objetivo de nuestro proyecto es hacer más fácil iniciar y controlar un período de enfoque desde Telegram.
>
> En esta versión ofrecemos temporizadores de enfoque de 5, 15 o 25 minutos. El bot avisa cuando termina el período para que la persona decida cuándo tomar su descanso.

**Aclaración para quien presenta:** hablar de la utilidad del método, sin explicar librerías, handlers ni código todavía.

### 3. ¿Qué puede hacer el bot y qué es `python-telegram-bot`? — 1 minuto — Persona 1, no técnica

**En pantalla:** el menú del bot y los comandos disponibles.

> Desde Telegram se puede iniciar un temporizador de 5, 15 o 25 minutos, cancelarlo y consultar estadísticas. También hay botones en el chat para acceder a las opciones.
>
> Para que Telegram y nuestro programa puedan comunicarse usamos `python-telegram-bot`. Podemos imaginarlo como un puente o traductor: ayuda a que el mensaje que enviamos en Telegram llegue al programa y que la respuesta del programa vuelva al chat.
>
> El bot es un apoyo sencillo para organizar períodos de trabajo. Esta versión automatiza el temporizador de enfoque; no inicia descansos automáticos.

### 4. ¿Qué hace `python-telegram-bot`? — 2 minutos — Persona 1, no técnica

**En pantalla:** un esquema sencillo: persona → Telegram → `Application` → handler → respuesta.

```text
Telegram envía una actualización
             ↓
         Application
             ↓
    handler que coincide
             ↓
       respuesta del bot
```

> Como comentamos, `python-telegram-bot` es el puente entre Telegram y nuestro programa. Cuando una persona envía un mensaje, Telegram lo entrega al bot como una actualización, es decir, como un aviso con la información de lo que ocurrió.
>
> La aplicación recibe ese aviso y lo dirige a la parte del programa que sabe responder. Por ejemplo, si llega `/start`, el bot muestra el saludo; si llega `/25`, inicia un temporizador de 25 minutos.
>
> El bot también consulta periódicamente a Telegram si hay mensajes nuevos. Así puede mantenerse atento mientras la persona usa el chat.

**Transición a la Persona 2:**

> Ya vimos cómo se comunica el bot a grandes rasgos. Ahora [nombre de Persona 2] mostrará las piezas concretas de la librería, el código y el funcionamiento del temporizador.

### 5. Preparar y ejecutar la aplicación — 1 minuto — Persona 2, técnica

**En pantalla:** recorte de `main.py`.

```python
application = ApplicationBuilder().token(token).build()
register_command_handlers(application)
register_timer_handlers(application)
application.run_polling()
```

> `ApplicationBuilder` construye la aplicación. Le pasamos el token para que sepa con qué bot de Telegram comunicarse y después registramos los handlers. Al final, `run_polling()` empieza a recibir actualizaciones.
>
> El token es una contraseña: se configura fuera del código y nunca se muestra en la pantalla compartida.

### 6. Componente 1: `CommandHandler` — 2 minutos — Persona 2, técnica

**En pantalla:** recorte de `commands.py`.

```python
application.add_handler(CommandHandler("start", start_command))
application.add_handler(CommandHandler("stats", stats_command))
```

> `CommandHandler` sirve para comandos con nombre, como `/start` o `/stats`. Le indicamos el nombre del comando y la función que queremos ejecutar.
>
> Esa función recibe `update` —lo que llegó— y `context` —información y herramientas disponibles para responder—. Como pide la librería, nuestros handlers son funciones `async` y usan `await` al enviar mensajes.

**Idea clave:** `CommandHandler` reconoce la forma de comando; la función asociada define qué significa para nuestro bot.

### 7. Componente 2: `MessageHandler` y filtros — 2 minutos — Persona 2, técnica

**En pantalla:** recorte de `timers.py`.

```python
application.add_handler(MessageHandler(filters.Regex(r"^/(5|15|25)\b"), start_timer))
```

> `/5`, `/15` y `/25` empiezan con un número, por eso el proyecto los recibe como mensajes y no como comandos normales. `MessageHandler` observa mensajes y `filters.Regex` deja pasar los que coinciden con la expresión regular.
>
> El filtro decide qué mensajes llegan a la función; `start_timer` obtiene los minutos e inicia el temporizador.

**Comparación rápida:** `/start` usa `CommandHandler`; `/25` usa `MessageHandler` con un filtro.

### 8. Componente 3: `JobQueue` y gestión de temporizadores — 3 minutos — Persona 2, técnica

**En pantalla:** recorte de `timers.py`.

```python
job = context.job_queue.run_once(timer_finished, minutes * 60, data=(key, minutes))
active_timers[key] = job
```

> `JobQueue` permite programar una función para más adelante. `run_once` la ejecuta una vez cuando pasa el tiempo indicado; en este caso, minutos convertidos a segundos.
>
> No es una fila FIFO de solicitudes de usuarios esperando turno. El proyecto permite un temporizador activo por `(chat_id, user_id)` y agenda un job independiente para cada combinación. Así, varias personas pueden tener temporizadores activos a la vez, pero la misma persona no puede iniciar otro en ese chat hasta cancelar el actual.
>
> La espera no se hace con `time.sleep`; la administra el scheduler de `JobQueue`, por lo que el bot puede seguir recibiendo mensajes. Cuando vence el job, `timer_finished` quita la sesión activa, registra los minutos completados en el CSV y envía el aviso. `/cancel` quita el job pendiente con `schedule_removal()`.
>
> Los handlers y callbacks que interactúan con Telegram son asíncronos. El temporizador activo se mantiene en memoria; si se reinicia el proceso, se pierde.

**Aclaración docente:** `JobQueue` programa el aviso; las reglas de quién puede iniciar otro temporizador pertenecen a nuestro código.

### 9. Componente 4: `ReplyKeyboardMarkup` y estadísticas — 1 minuto — Persona 2, técnica

**En pantalla:** una captura del menú del bot.

> `ReplyKeyboardMarkup` muestra botones en el chat. Al tocar `/25`, Telegram envía ese texto como mensaje y la aplicación reutiliza el mismo handler numérico. El teclado facilita el uso, pero no reemplaza la lógica del comando.
>
> Las estadísticas se guardan en un archivo CSV con fecha, chat, usuario y minutos. El handler de `/stats` recibe el comando y las funciones del proyecto calculan los totales.

### 10. Demostración del código y funcionamiento — 3 minutos — Persona 2, técnica

1. Enviar `/start` y mostrar el teclado.
2. Enviar `/5` y señalar la respuesta de inicio.
3. Cancelar con `/cancel`, sin esperar cinco minutos.
4. Mostrar en el código el `MessageHandler`, el `run_once` de `JobQueue` y `timer_finished`.
5. Si hay tiempo, enviar `/stats` y aclarar que el comando se recibe con PTB, pero el cálculo y el archivo CSV son código del proyecto.

**Plan alternativo:** si Telegram o la conexión no están disponibles, mostrar capturas y los tres fragmentos de código anteriores. Nunca mostrar el token.

### 11. Cierre y preguntas — 2 minutos — Ambas personas

> **Persona 1:** En resumen, el bot facilita iniciar un período de enfoque y recibir un aviso al terminar.
>
> **Persona 2:** Técnicamente, `Application` recibe y distribuye actualizaciones; `CommandHandler` y `MessageHandler` seleccionan funciones para distintos mensajes; `JobQueue` programa una acción futura; y `ReplyKeyboardMarkup` ofrece botones. La librería aporta el mecanismo de comunicación y nuestra aplicación define las reglas.

Preguntas que pueden hacer:

- ¿Qué diferencia hay entre `CommandHandler` y `MessageHandler`?
- ¿Por qué no usamos `time.sleep` en un bot?
- ¿Qué parte del ejemplo pertenece a `python-telegram-bot` y qué parte escribimos nosotros?
- ¿Qué pasa si se reinicia el proceso mientras hay un temporizador activo?

## Preparación

- [ ] Completar los nombres de ambas personas.
- [ ] La Persona 1 ensaya la introducción sin tecnicismos; la Persona 2 ensaya el recorrido del código y la demostración.
- [ ] Mantener las cámaras encendidas durante la exposición y compartir pantalla.
- [ ] Tener el bot configurado; no mostrar el token.
- [ ] Ensayar para que el total no supere los 20 minutos.
- [ ] Preparar capturas por si falla la demostración en vivo.

## Apoyo para preguntas de defensa: herramientas del proyecto

> Esta parte es material de respaldo para responder preguntas; no suma al bloque de 20 minutos sobre `python-telegram-bot`.

### ¿Qué significa un registro `INFO httpx` con `POST .../bot<TOKEN>/getUpdates` y `200 OK`?

`python-telegram-bot` usa HTTP para consultar a Telegram mediante *long polling*. `getUpdates` es la consulta de actualizaciones y `200 OK` indica que la solicitud HTTP se procesó correctamente; no necesariamente significa que haya llegado un mensaje nuevo. El token aparece dentro de la URL, así que no se debe mostrar ni compartir el registro completo. Si el token se expone, hay que revocarlo en BotFather, generar otro, actualizar `.env` y reiniciar el bot.

### ¿Cómo se gestiona la cola de temporizadores?

`JobQueue` agenda el callback de cada temporizador; no es una fila FIFO de usuarios esperando su turno. El diccionario `active_timers` guarda un temporizador por `(chat_id, user_id)`, y `run_once` agenda el aviso para cada combinación. Al vencer, `timer_finished` quita la sesión activa, registra los minutos en el CSV y avisa al usuario. `/cancel` elimina tanto la sesión como el job pendiente. El estado está en memoria y se pierde si se reinicia el bot.

### ¿Cómo se instala y ejecuta?

Las dependencias están en `requirements.txt` y se instalan con `pip`. Después se arranca el bot con Python:

```bash
pip install -r requirements.txt
python main.py
```

### Diferencia rápida

| Herramienta | Para qué se usa |
| --- | --- |
| `python-telegram-bot` | Recibir mensajes, procesar actualizaciones y responder en Telegram. |
| `pip` | Instalar las dependencias del proyecto. |
| Docker | Ejecutar el bot dentro de un contenedor (opcional). |
