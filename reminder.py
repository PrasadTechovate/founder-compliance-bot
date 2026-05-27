import os
import json
import requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
founders = json.loads(os.getenv("FOUNDERS_JSON","[]"))

today = datetime.utcnow().date()


def send(chat_id,message):

    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id":chat_id,
            "text":message
        }
    )


with open("compliance.json") as f:
    data=json.load(f)

tasks=[]

for item in data["monthly"]:

    event_date=datetime(
        today.year,
        today.month,
        item["day"]
    ).date()

    tasks.append({
        "title":item["title"],
        "date":event_date.strftime("%Y-%m-%d")
    })

for item in data["yearly"]:
    tasks.append(item)

reminders=[]

for task in tasks:

    event_date=datetime.strptime(
        task["date"],
        "%Y-%m-%d"
    ).date()

    diff=(event_date-today).days

    if diff in [7,3,1,0]:

        if diff==0:
            reminders.append(
                f"⚠️ TODAY: {task['title']}"
            )

        else:

            reminders.append(
                f"{task['title']} ({diff} days)"
            )

if reminders:

    message=(
        "📌 Compliance Reminder\n\n"+
        "\n".join(reminders)
    )

    for founder in founders:

        send(
            founder["chat_id"],
            message
        )
