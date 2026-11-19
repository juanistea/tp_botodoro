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


def get_stats(chat_id, user_id):
    stats = {
        "today_pomodoros": 0,
        "today_minutes": 0,
        "total_pomodoros": 0,
        "total_minutes": 0,
    }

    if not os.path.exists(STATS_FILE):
        return stats

    today = date.today().isoformat()

    with open(STATS_FILE, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            # Solo contamos las filas de esta persona en este chat
            if int(row["chat_id"]) != chat_id or int(row["user_id"]) != user_id:
                continue

            minutes = int(row["minutes"])
            stats["total_minutes"] += minutes
            if minutes == 25:
                stats["total_pomodoros"] += 1

            if row["date"] == today:
                stats["today_minutes"] += minutes
                if minutes == 25:
                    stats["today_pomodoros"] += 1

    return stats
