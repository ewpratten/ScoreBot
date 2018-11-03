import requests
import random

def formatTweetAction(username, wl, match_key, event_name):
	output =  f"@{username} has just {wl} {match_key} at {event_name}."
	if wl == "won":
		rand_list = [" Good job!", " Nice work!", " Go team!"]
		output += str(random.choice(rand_list))
	return output

def send(webhook, message):
	# payload = {"text": message}
	payload = message
	
	response = requests.post(webhook, data=str(payload), headers={"Content-Type":"application/json"})
	if response.status_code != 200:
		print("Could not send message to slack")
		print(response)

def formatSend(webhook, data, twitter_username):
	if data["winning_alliance"] == data["alliance"]:
		wl = "won"
	else:
		wl = "lost"
	
	intent_base = "https://twitter.com/intent/tweet?hashtags=omgrobots&text="
	
	fallback = "We have "+ wl +" "+ str(data["match_number"])
	
	if wl == "won":
		win_badge = ":tada:"
	else:
		win_badge = ""
	
	payload = {
		"attachments" : [{
			"fallback":fallback,
			"author_name":"The Blue Alliance",
			"author_link":"https://www.thebluealliance.com",
			"author_icon":"https://www.thebluealliance.com/images/tba_lamp.svg",
			"title":"Match Results "+ win_badge,
			"text":"For "+ str(data["match_number"]) +" at "+ str(data["event_key"]),
			"color": "#3AA3E3",
			"fields":[
				{
				"title":"Blue Score",
				"value":str(data["blue_score"]),
				"short": True
			},
			{
				"title":"Red Score",
				"value":str(data["red_score"]),
				"short": True
			}
			],
			"actions":[
				{
					"type":"button",
					"name":"action",
					"text":"View More",
					"url":"https://www.thebluealliance.com/event/"+ str(data["event_key"]),
					"style":"primary"
				},
				{
					"type":"button",
					"name":"action",
					"text":"Share",
					"url":intent_base+ formatTweetAction(twitter_username.split("@")[:-1], wl, str(data["match_number"]), str(data["event_name"]))
				}
				]
		}]
	}
	
	send(webhook, payload)
