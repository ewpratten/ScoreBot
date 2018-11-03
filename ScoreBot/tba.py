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
	
	return requests.get(tba_api + "/team/"+ team_key +"/event/"+ event_key +"/matches", params={"X-TBA-Auth-Key":tba_key}).json()

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
	
	return output
	