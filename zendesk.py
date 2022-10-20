from datetime import datetime
import requests

from apitokens import apikeys


ASSIGNEES = { 
    "Kevan": 1904692543967,
    "Dan": 1905120774787,
    "Brian": 0
}

HEADERS = {
  'Authorization': apikeys()["ZENDESK_TOKEN"],
  'Accept': 'application/json',
  'Cookie': '__cfruid=4f9bbf0388bc296bbc168a837777feb7f1c70eb6-1663960636; _zendesk_cookie=BAhJIhl7ImRldmljZV90b2tlbnMiOnt9fQY6BkVU--459ed01949a36415c1716b5711271c3d08918307'
}


def sendrequest(rtype,url,payload=None):
    """Send HTTP Request"""

    if payload is None:
        payload={}

    response = requests.request(rtype, url, headers=HEADERS, data=payload)
    
    return(response.json())


def get_alltickets():
    """Get all tickets from Zendesk"""

    alltickets = []

    url = "https://sevenroomsit.zendesk.com/api/v2/tickets.json"

    while url != None:

        request = sendrequest("GET",url,payload=None)
        alltickets.append(request["tickets"])
        url = request["next_page"]
    
    return alltickets


def get_allassignedtickets(assignee_id):
    url = "https://sevenroomsit.zendesk.com/api/v2/users/%s/tickets/assigned.json" % (assignee_id)
    request = sendrequest("GET",url,payload=None)

    return request

def get_allticketsmetrics():
    url = "https://sevenroomsit.zendesk.com/api/v2/ticket_metrics.json"
    request = sendrequest("GET",url,payload=None)

    return request


def get_ticketdetails(ticket_id):
    url = "https://sevenroomsit.zendesk.com/api/v2/tickets/%s" % ticket_id
    request = sendrequest("GET", url, payload=None)

    return request

def cleandate(date_):
    date_ = date_.split("T")
    date_ = date_[0].split("-")
    cleaneddate = datetime(int(date_[0]),int(date_[1]),int(date_[2]))


    return cleaneddate

def grab_userassignedtickets(user_,checkdate_=None):
    """Grab list of all tickets completed by a user"""

    completed_tickets = {}

    if checkdate_ is None:
        checkdate_ = datetime.now()
    today = checkdate_
    print("CHECKING",user_,today)

    alltickets = get_allticketsmetrics()
    alltickets = alltickets["ticket_metrics"]

    for ticket in alltickets:
        if ticket["solved_at"]:
            cleaneddate = cleandate(ticket["solved_at"])

            # Check if difference is not greater than zero between today and solve date
            if "day" not in str(today - cleaneddate):
                ticket_id = ticket["ticket_id"]
                ticket_details = (get_ticketdetails(ticket_id))["ticket"]
                subject = ticket_details["subject"]
                assignedto = ticket_details["assignee_id"]
                ticket_tags = ticket_details["tags"]
                #print(ticket_details)

                if assignedto == ASSIGNEES[user_]:

                    completed_tickets[str(ticket_id)] =  subject

    
    return completed_tickets

if __name__ == '__main__':  

    targetdate = datetime(2022,10,19)


    kev_tickets = grab_userassignedtickets("Kevan",targetdate)
    print(len(kev_tickets))

    for ticket in kev_tickets:
        print(ticket)

    dan_tickets = grab_userassignedtickets("Dan",targetdate)

    for ticket in dan_tickets:
        print(ticket)

