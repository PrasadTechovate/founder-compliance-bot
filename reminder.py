import os
import json
import requests
from datetime import datetime

timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

log_file = f"debug_{timestamp}.txt"

logs=[]

def log(msg):

    now=datetime.utcnow().strftime("%H:%M:%S")

    line=f"[{now}] {msg}"

    logs.append(line)


log("===== BOT STARTED =====")


BOT_TOKEN=os.getenv("BOT_TOKEN")

founders_raw=os.getenv(
    "FOUNDERS_JSON",
    "[]"
)

log(
    f"BOT TOKEN EXISTS: "
    f"{BOT_TOKEN is not None}"
)

log(
    f"FOUNDERS RAW: "
    f"{founders_raw}"
)

founders=json.loads(
    founders_raw
)

log(
    f"FOUNDERS COUNT: "
    f"{len(founders)}"
)

today=datetime.utcnow().date()

log(
    f"TODAY UTC: {today}"
)


def send(chat_id,message):

    log(
        f"Sending to "
        f"{chat_id}"
    )

    url=(
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}"
        f"/sendMessage"
    )

    response=requests.post(
        url,
        data={
            "chat_id":chat_id,
            "text":message
        }
    )

    log(
        f"Telegram Status:"
        f"{response.status_code}"
    )

    try:

        log(
            f"Telegram response:"
            f"{response.json()}"
        )

    except:

        log(
            "Telegram parse error"
        )


log(
    "Loading compliance.json"
)

with open(
    "compliance.json"
) as f:

    data=json.load(f)


log(
    "Compliance loaded"
)

tasks=[]


for item in data["monthly"]:

    event_date=datetime(
        today.year,
        today.month,
        item["day"]
    ).date()

    task={

        "title":
        item["title"],

        "date":
        event_date.strftime(
            "%Y-%m-%d"
        )
    }

    tasks.append(task)

    log(
        f"Monthly task:"
        f"{task}"
    )


for item in data["yearly"]:

    tasks.append(item)

    log(
        f"Yearly task:"
        f"{item}"
    )


reminders=[]


for task in tasks:

    event_date=datetime.strptime(
        task["date"],
        "%Y-%m-%d"
    ).date()

    diff=(
        event_date-today
    ).days


    log(
        f"{task['title']} "
        f"diff={diff}"
    )


    # testing mode
    if diff>=0:

        if diff==0:

            msg=(
                f"⚠️ TODAY:"
                f"{task['title']}"
            )

        else:

            msg=(
                f"{task['title']}"
                f" ({diff} days)"
            )

        reminders.append(msg)


log(
    f"REMINDERS:"
    f"{len(reminders)}"
)


if reminders:

    message=(
        "📌 Compliance Reminder\n\n"
        +
        "\n".join(reminders)
    )


    for founder in founders:

        send(
            founder["chat_id"],
            message
        )

else:

    log(
        "No reminders"
    )


log(
    "===== BOT FINISHED ====="
)


with open(
    log_file,
    "w",
    encoding="utf-8"
) as f:

    for row in logs:

        f.write(
            row+"\n"
        )
