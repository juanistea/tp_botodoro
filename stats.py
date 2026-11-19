import csv
import os
from datetime import date

STATS_FILE = os.getenv("STATS_FILE", "data/stats.csv")


def record_timer(chat_id, user_id, minutes):
    # Agrega una fila al CSV cada vez que termina un temporizador
    os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
    new_file = not os.path.exists(STATS_FILE)

    with open(STATS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["date", "chat_id", "user_id", "minutes"])
        writer.writerow([date.today().isoformat(), chat_id, user_id, minutes])

