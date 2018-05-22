"""
 Code to retrieve messages in a group chat
 """
import time
import requests
from groupme.bot import bot_properties

# GroupMe token
REQUEST_PARAMS = {'token': bot_properties.GROUP_ME_TOKEN}

# location information for weather bot
LOCATION_NAME = 'Austin, TX'
LOCATION_COORDS = {'x': '30.18', 'y': '-97'}

# Checks the group chat every 5 seconds for new messages for the bot to respond to
while True:
	# The messages from the chat
	RESPONSE = (requests.get('https://api.groupme.com/v3/groups/40284150/messages',
                          params=REQUEST_PARAMS))
	if RESPONSE.status_code == 200:
		RESPONSE_MESSAGES = RESPONSE.json()['response']['messages']

	# Checks if any of the retrieved messages contain the  phrase 'Weatherbot'
	for message in RESPONSE_MESSAGES:
		if message['text'] == 'WeatherBot':
			weather_response = (requests.get('https://api.weather.gov/points/' + LOCATION_COORDS['x'] + ','
                                    + LOCATION_COORDS['y'] + '/forecast').json())
			current_weather = weather_response['properties']['periods'][0]['detailedForecast']
			to_send = 'Weather for ' + LOCATION_NAME + ': ' + current_weather
			post_params = {'bot_id' : 	bot_properties.BOT_ID, 'text': to_send}
			requests.post('https://api.groupme.com/v3/bots/post', params=post_params)
			REQUEST_PARAMS['since_id'] = message['id']
			break
	time.sleep(5)
