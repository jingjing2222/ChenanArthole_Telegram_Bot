import logging
import pytz
from datetime import datetime, timedelta
import requests
import telegram
import azure.functions as func

my_token = '' # Telegram API
chat_id =  # Telegram Chating room ID
token = "" # Notion API TOKEN
databaseId = "" # Database ID
bot = telegram.Bot(token=my_token)

def sendmessage(text):
    bot.send_message(chat_id, text)

def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    sortParams = {
        "sorts": [
            {
                "property": "근무일시",
                "direction": "descending"
            }
        ]
    }

    res = requests.post(readUrl, headers=headers, json=sortParams)
    data = res.json()
    korea_tz = pytz.timezone('Asia/Seoul')

    today = datetime.now(korea_tz)
    tomorrow = today + timedelta(days=1)
    check=0
    messages = '스케줄 확인합니다!\n'
    people = ''
    for result in data['results']:
        if '근무일시' in result['properties'] and result['properties']['근무일시']['date'] is not None:
            work_date = datetime.strptime(result['properties']['근무일시']['date']['start'], "%Y-%m-%dT%H:%M:%S.%f%z")

            if work_date.date() == tomorrow.date():
                check = 1
                attendance_time = work_date - timedelta(hours=1, minutes=20)
                show = result['properties']['공연명']['title'][0]['text']['content']
                location = result['properties']['공연장분류']['select']['name']
                runningtime = result['properties']['러닝타임']['rich_text'][0]['text']['content']
                personnel_list = [person['name'] for person in result['properties']['근무인원']['multi_select']]
                sorted_personnel = sorted(personnel_list, key=lambda x: x.encode('unicode_escape'))  # Sorting in Korean alphabetical order

                people = ' '.join(sorted_personnel)

                content = f'\n[{location}]\n공연명: {show}\n공연 일시: {work_date.date()} {work_date.strftime("%H:%M")}\n러닝타임(인터미션): {runningtime}\n출근시각: {attendance_time.strftime("%H:%M")}\n\n{people}'
                messages += content
                messages += '\n'
    if check == 0:
        messages += '다음 날 공연이 없습니다'
    messages += '\n\n'

    return messages

headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2022-02-22"
}
app = func.FunctionApp()

@app.schedule(schedule="0 0 23 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def TimerTrigger(myTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.utcnow().replace(
        tzinfo=pytz.utc).isoformat()

    messages = readDatabase(databaseId, headers)
    sendmessage(messages)

    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
