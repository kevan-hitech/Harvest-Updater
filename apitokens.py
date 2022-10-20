
def apikeys():
    """ Insert API keys wrap all tokens in "double quotes" """

    TOKENS = {
        # Slack - Test
        "SLACK_TESTCHANNEL" : "",
        "SLACK_TESTBOTTOKEN" : "",

        # Slack - Prod
        "SLACK_CHANNEL" : "",
        "SLACK_BOTTOKEN" : "",

        # Harvest
        "HARVEST_TOKEN" : "",

        # Zendesk
        "ZENDESK_TOKEN" : "",
    }

    return TOKENS
