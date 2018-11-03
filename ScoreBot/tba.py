import requests

def getEventKeys(tba_key, tba_api, team):
	team_key = "frc"+str(team)
	
	raw_data = requests.get(tba_api + "/team/"+ team_key +"/events", params={"X-TBA-Auth-Key":tba_key}).json()
	
	output = []
	for event in raw_data:
		output.append(event["key"])
	
	return output
	
def getEventData(tba_key, tba_api, event_key, team):
	team_key = "frc"+str(team)
	
	output = requests.get(tba_api + "/team/"+ team_key +"/event/"+ event_key +"/matches", params={"X-TBA-Auth-Key":tba_key}).json()
	event = requests.get(tba_api + "/event/"+ str(event_key), params={"X-TBA-Auth-Key":tba_key}).json()
	output["event_name"] = event["short_name"]
	output["webcasts"] = event["webcasts"]
	return 

def parseMatch(team, match):
	team_key = "frc"+str(team)
	
	output = {}
	
	output["match_time"] = match["actual_time"]
	
	# Construct match out of key
	match_id = str(match["key"].split("_")[1])
	match_id = match_id.replace("m", " match ")
	output["match_number"] = match_id
	
	output["event_key"] = match["event_key"]
	
	output["blue_score"] = match["alliances"]["blue"]["score"]
	output["red_score"] = match["alliances"]["red"]["score"]
	
	# Detect what alliance we are
	if team_key in match["alliances"]["blue"]:
		output["alliance"] = "blue"
	else:
		output["alliance"] = "red"
	
	output["winning_alliance"] = match["winning_alliance"]
	output["event_name"] = match["event_name"]
	
	output["webcast"] = "https://www.thebluealliance.com/gameday/"+ output["event_key"]
	for cast in match["webcasts"]:
		if cast["type"] == "twitch":
			output["webcast"] = "https://twitch.tv/"+ cast["channel"]
	output["blue_teams"] = ""
	output["red_teams"] = ""
	
	for team in match["alliances"]["blue"]["team_keys"]:
		output["blue_teams"] += team[3:] + "\n"
		
	for team in match["alliances"]["red"]["team_keys"]:
		output["red_teams"] += team[3:] + "\n"
			
	
	return output
	
