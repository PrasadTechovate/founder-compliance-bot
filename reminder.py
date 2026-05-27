import os
import json
import requests
from datetime import datetime

print("NEW VERSION LOADED")

timestamp = datetime.utcnow().strftime(
    "%Y-%m-%d_%H-%M-%S"
)

log_file = f"debug_{timestamp}.txt"

logs=[]


def log(msg):

    now=datetime.utcnow().strftime(
        "%H:%M:%S"
    )

    logs.append(
        f"[{now}] {msg}"
    )


log("===== BOT STARTED =====")


BOT_TOKEN=os.getenv(
    "BOT_TOKEN"
)

founders=json.loads(
    os.getenv(
        "FOUNDERS_JSON",
        "[]"
    )
)

today=datetime.utcnow().date()

log(f"TODAY:{today}")



def send(chat_id,message):

    url=(
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    response=requests.post(
        url,
        data={
            "chat_id":chat_id,
            "text":message
        }
    )

    log(
        f"Sent->{chat_id}"
    )

    log(
        f"Status:{response.status_code}"
    )

    try:

        log(
            response.text
        )

    except:

        log(
            "response parse error"
        )



with open(
    "compliance.json"
) as f:

    data=json.load(f)


tasks=[]


####################################
# MONTHLY TASKS
####################################

for item in data["monthly"]:

    month=today.month
    year=today.year

    event_date=datetime(

        year,
        month,
        item["day"]

    ).date()


    if event_date<today:

        month+=1

        if month>12:

            month=1
            year+=1


        event_date=datetime(

            year,
            month,
            item["day"]

        ).date()


    task=item.copy()

    task["date"]=(
        event_date.strftime(
            "%Y-%m-%d"
        )
    )

    task["source"]="monthly"

    tasks.append(task)

    log(
        f"Monthly:{task}"
    )



####################################
# YEARLY TASKS
####################################

for item in data["yearly"]:


    event_date=datetime(

        today.year,

        item["month"],

        item["day"]

    ).date()


    if event_date<today:

        event_date=datetime(

            today.year+1,

            item["month"],

            item["day"]

        ).date()


    task=item.copy()

    task["date"]=(
        event_date.strftime(
            "%Y-%m-%d"
        )
    )

    task["source"]="yearly"

    tasks.append(task)

    log(
        f"Yearly:{task}"
    )



####################################
# BUILD REMINDERS
####################################


message_parts=[]


for task in tasks:


    event_date=datetime.strptime(

        task["date"],

        "%Y-%m-%d"

    ).date()


    diff=(
        event_date-today
    ).days


    log(
        f"{task['title']} diff={diff}"
    )


    show=False


    ################################
    # MONTHLY
    ################################

    if task["source"]=="monthly":

        if 0<=diff<=10:

            show=True


    ################################
    # YEARLY
    ################################

    elif task["source"]=="yearly":

        if diff>=0:

            show=True



    if show:


        if diff==0:

            msg=(
                "⚠ TODAY\n"
            )

        else:

            msg=(
                f"⏳ {diff} days left\n"
            )


        msg+=(
            f"\n"
            f"Category: "
            f"{task['category']}\n\n"

            f"Task: "
            f"{task['title']}\n\n"

            f"Note: "
            f"{task['note']}"
        )


        message_parts.append(
            msg
        )



####################################
# SEND
####################################


if message_parts:


    final_message=(

        "📌 Founder Compliance\n\n"

        +

        "\n\n----------------\n\n".join(

            message_parts

        )

    )


    log(
        "Sending final message"
    )


    for founder in founders:


        send(

            founder["chat_id"],

            final_message

        )


else:

    log(
        "No reminders today"
    )



####################################
# DEBUG
####################################


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


print(
    f"DEBUG FILE CREATED:{log_file}"
)
