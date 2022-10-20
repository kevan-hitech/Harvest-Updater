import requests, datetime
from apitokens import apikeys

# Harvest API
BASE_URL = "https://api.harvestapp.com/api/v2/"

PAYLOAD={}

HEADERS = {
  'Harvest-Account-Id': '507529',
  'Authorization': apikeys()["HARVEST"]
}

USERS = {
"Dan": 4100799,
"Kevan": 3913388
}

def sendrequest(request_type,url_):
    """Send HTTP Request to the Harvest API"""
    url = BASE_URL + url_
    response = requests.request(request_type, url, headers=HEADERS, data=PAYLOAD)

    return response.json()


def generate_dates():
    """Based on today's date generate specific date values"""
    pass

def parse_entries(date_=None):
    """Get all entries within a certain range"""
    
    if date_ is None:
        date_ = generate_dates



def get_entries(user_, dates):
    """Receive Harvest entries within a certain range"""

    user_id = USERS[user_]
    from_ = dates[0]
    to_ = dates[-1]

    url = "time_entries.json?user_id=%s&from=%s&to=%s" % (user_id, from_, to_)
    entries = sendrequest("GET",url)

    return entries["time_entries"]


def check_hours(entries):
    """Check if entry time equals at least 7 hours"""

    total_time = 0
    for entry in (entries):
        #print(entry)

        client_ = entry["client"]["name"]
        project_ = entry["project"]["name"]
        task_ = entry["task"]["name"]
        time_ = entry["hours"]
        notes_ = entry["notes"]

        print(client_, project_, task_, time_)
        print("~~~~\n"+notes_,"\n")
        total_time += time_
    
    print(total_time)

    if total_time >= 7:
        return (True,)
    else:
        return (False,total_time)


def addtime(ticket_num):
    """Generate time to complete tickets"""

    tickets_done = ticket_num * .25
    start = datetime.datetime(2000,1,1,12,0,0)
    end = start + datetime.timedelta(hours=tickets_done)
    end = end.strftime("%H:%M")

    return end
    
def addnotes(zendesk_):
    """Get notes from the tickets to add to Zendesk"""

    notes_ = ""
    for a,b in zendesk_.items():
        notes_ += "- Zendesk | %s: %s\n" % (a,b)
    
    return notes_






def add_tickets(user_, dates_,zendesk_tickets):
    """Add Harvest entry"""    
    
    
    project_id = "28900951"
    task_id = "17510689"
    spend_date = str(dates_).split(" ")[0]
    user_id = USERS[user_]



    start_time = "12:00am"
    end_time = addtime(len(zendesk_tickets)) + "am"
    notes = addnotes(zendesk_tickets)

    url = "time_entries?project_id=%s&task_id=%s&spent_date=%s&user_id=%s&started_time=%s&ended_time=%s&notes=%s" % (project_id, task_id, spend_date, user_id, start_time, end_time, notes)
    print(url)
    sendrequest("POST",url)


if __name__ == '__main__':
    
    print("HARVEST.PY")
    dates = ("2022-10-18","2022-10-18")
    ent = get_entries("Dan", dates)
    print(check_hours(ent))
    print("HARVEST.PY")
    





    

