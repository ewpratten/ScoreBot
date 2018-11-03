import tba as tba
import slack as slack

config = eval(open("./CONFIG.json", "r").read())

# TEST
print(config)

# print(tba.getEventKeys(config["tba_key"], config["tba_endpoint"], config["team_number"]))

all_matches = tba.getEventData(config["tba_key"], config["tba_endpoint"], config["event_key"], config["team_number"])
newest_match = all_matches[0]
parsed_match = tba.parseMatch(config["team_number"], newest_match)
slack.formatSend(config["slack_webhook_url"], parsed_match)

