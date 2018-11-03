import requests

def send(webhook, message):
	payload = {"text": message}
	
	response = requests.post(webhook, data=payload, headers={"Content-Type":"application/json"})
	if response.status_code != 200:
		print("Could not send message to slack")