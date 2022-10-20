import re, time
import zendesk, slack, harvest
from datetime import datetime, timedelta

def getdates():
    """Using today's date - get all dates up from Monday"""
    date_ = datetime.now()
    weeknumber = (date_.strftime("%u"))

    delta = int(weeknumber) - 1
    # If checking on Monday, grab last week
    if delta == 0:
        startdate = date_ - timedelta(days=3)
        startdate = str(startdate).split(" ",maxsplit=1)[0]
        delta = 5
    else:
        startdate = date_ - timedelta(days=delta)
        startdate = str(startdate).split(" ",maxsplit=1)[0]

    dates = []
    for i in range(delta):
        add_date = startdate.split("-")
        add_date[2] = str(int(add_date[2])+i)
        add_date = add_date[0]+"-"+add_date[1]+"-"+add_date[2]
        print(add_date)
        dates.append(add_date)
    
    return dates


def checkhours(whomst):
    """Create Slack message - based on hour requirements"""

    hour_prompt = ""

    dates = getdates()
    for date_ in dates:
        harvest_entries = harvest.get_entries(whomst, [date_])
        harvest_hourcheck = harvest.check_hours(harvest_entries)
        if not harvest_hourcheck[0]:
            hour = harvest_hourcheck[1]
            hour_prompt += "  •  " + date_ + " - " + str(hour) + " hrs\n"

    if len(hour_prompt) != 0:
        hour_prompt = "Hey <@U02UE37F0QM>,\nPlease add notes for the following days:\n" + hour_prompt

    return (hour_prompt)

def addzentickets(whomst):
    """Add Zendesk tickets to Harvest, if they aren't already added."""
    date_o = datetime.now()
    date_ = str(date_o).split(" ", maxsplit=1)[0]

    # Grab harvest and zendesk Entries
    harvest_entries = harvest.get_entries(whomst, [date_])
    date_ = date_.split("-")
    date_d = datetime(int(date_[0]),int(date_[1]),int(date_[2]))
    zendesk_tickets = zendesk.grab_userassignedtickets(whomst,date_d)

    for entry in harvest_entries:
        client = entry["client"]["name"]
        project = entry["project"]["name"]
        note = entry["notes"]
        print(client,project,"\n",note)

        found = re.findall(r"[0-9]{4}",note)
        
        for ticket in found:
            if ticket in zendesk_tickets:
                zendesk_tickets[ticket] = False
    
    already_added = []
    # Any items not already added add to harvest
    for ticket_id,ticket_desc in zendesk_tickets.items():
        if ticket_desc is False:
            already_added.append(ticket_id)
    
    for item in already_added:
        del zendesk_tickets[item]
    
    if len(zendesk_tickets) > 0:
        harvest.add_tickets(whomst,date_d,zendesk_tickets)

    return zendesk_tickets


def slacktickets(tickets):
    """Send message about tickets added to Harvest"""
    if len(tickets) > 0:
        prompt = "The following tickets have been added to your harvest - please review:\n"
        for ticket,subject in tickets.items():
            url = "https://sevenroomsit.zendesk.com/agent/tickets/%s" % (ticket)
            prompt += "  •  <%s|zendesk #%s> - %s\n" % (url,ticket,subject)

    return prompt

if __name__ == '__main__':

    while True:
        today_ = (datetime.now()).strftime("%Y/%m/%d: %H:%M")
        hour_ = int((datetime.now()).strftime("%H"))
        
        # Initate at 12:00 PM
        if hour_ == 12:
            slack.sendslack(checkhours("Dan"))
            time.sleep(4500)

        # Initiate at 6:00PM
        if hour_ == 18:
            k_tickets = addzentickets("Kevan")
            d_tickets = addzentickets("Dan")
            slack.sendslack(slacktickets(d_tickets))
            time.sleep(42300)

        print(today_)
        time.sleep(900)
    