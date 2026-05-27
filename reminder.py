import os
import json
import requests
from datetime import datetime

print("===== BOT STARTED =====")

BOT_TOKEN = os.getenv("BOT_TOKEN")
founders_raw = os.getenv("FOUNDERS_JSON","[]")

print("BOT_TOKEN loaded:", BOT_TOKEN is not None)
print("FOUNDERS_JSON raw:")
print(founders_raw)

founders = json.loads(founders_raw)

print("Founders count:", len(founders))

today = datetime.utcnow().date()

print("UTC date:", today)


def send(chat_id,message):

    print(f"\nSending message to {chat_id}")

    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response=requests.post(
        url,
        data={
            "chat_id":chat_id,
            "text":message
        }
    )

    print("Telegram status:",response.status_code)

    try:
        print("Telegram response:",response.json())
    except:
        print("Could not parse response")


print("\nLoading compliance.json")

with open("compliance.json") as f:
    data=json.load(f)

print("Loaded JSON:")
print(json.dumps(data,indent=2))


tasks=[]

print("\nGenerating monthly tasks")

for item in data["monthly"]:

    event_date=datetime(
        today.year,
        today.month,
        item["day"]
    ).date()

    generated_task={
        "title":item["title"],
        "date":event_date.strftime("%Y-%m-%d")
    }

    tasks.append(generated_task)

    print("Added monthly task:")
    print(generated_task)


print("\nAdding yearly tasks")

for item in data["yearly"]:

    tasks.append(item)

    print("Added yearly task:")
    print(item)


print("\nTotal tasks:",len(tasks))

reminders=[]

print("\nChecking reminders")

for task in tasks:

    event_date=datetime.strptime(
        task["date"],
        "%Y-%m-%d"
    ).date()

    diff=(event_date-today).days

    print(
        f"Task: {task['title']} | "
        f"Date: {event_date} | "
        f"Diff:{diff}"
    )

    # TEST MODE
    if diff >=0:

        if diff==0:

            msg=f"⚠️ TODAY: {task['title']}"

        else:

            msg=f"{task['title']} ({diff} days)"

        reminders.append(msg)

        print("Reminder added:")
        print(msg)


print("\nFinal reminders:")

for r in reminders:
    print(r)


if reminders:

    message=(
        "📌 Compliance Reminder\n\n"+
        "\n".join(reminders)
    )

    print("\nMessage to send:")
    print(message)

    for founder in founders:

        print(
            "\nFounder:",
            founder
        )

        send(
            founder["chat_id"],
            message
        )

else:

    print("\nNo reminders today")


print("\n===== BOT FINISHED =====")
