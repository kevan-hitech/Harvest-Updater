from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from apitokens import apikeys

def sendmessage(channel_,message,BOTTOKEN):
    """Send message to Slack"""
    client = WebClient(token=BOTTOKEN)

    try:
        client.chat_postMessage(channel=channel_, text=message)
    except SlackApiError as error:
        # You will get a SlackApiError if "ok" is False
        assert error.response["ok"] is False
        assert error.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {error.response['error']}")

def uploadfile(channel_,path_,BOTTOKEN):
    """Upload item to Slack"""
    client = WebClient(token=BOTTOKEN)

    try:
        response = client.files_upload(channels=channel_, file=path_)
        assert response["file"]  # the uploaded file
    except SlackApiError as error:
        # You will get a SlackApiError if "ok" is False
        assert error.response["ok"] is False
        assert error.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {error.response['error']}")

def sendslack(mes):
    """Send message to appropriate Slack channel"""
    DEBUG = False

    if DEBUG:
        channel = apikeys()["SLACK_TESTCHANNEL"]
        BOTTOKEN = apikeys()["SLACK_TESTBOTTOKEN"]
    else:
        channel  = apikeys()["SLACK_CHANNEL"]
        BOTTOKEN = apikeys()["SLACK_BOTTOKEN"]

    sendmessage(channel,mes,BOTTOKEN)


if __name__ == "__main__":
    print("Slack.py Main")