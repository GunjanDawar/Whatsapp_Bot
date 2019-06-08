import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secret.json"
import requests, json 
# from emojipedia import Emojipedia, Emoji
from googletrans import Translator

translator = Translator()

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "news-chat-bot-iycwtd"

from gnewsclient import gnewsclient

client = gnewsclient.NewsClient()


	# emoji1=emoji.emojize('Python is :thumbs_up:')

	# return emoji

# def receive_message():
#    # Get the description for this parameters
#    parameters = request.values.get('Body')
   
#    description = get_emojipedia_description(parameters)
#    send_message(to=request.values['From'], body=description)

#    return ('', 204)

# # Helper function to get an emoji's description
# def get_emojipedia_description(parameters):
#    # Get the Emojipedia page for this emoji

# 	print(parameters)
# 	category= parameters.get('emoji_category','animal')
# 	date1=parameters.get('time','5:00')
# 	session = HTMLSession()
# 	response = session.get('https://emojipedia.org/' + parameters)

#    # If we didn't find an emoji, say so
# 	if not response.ok:
# 		return "Hmm - I couldn't find that emoji. Try sending me a single emoji ☝️"

# 	else:
# 		return category,date

   # Extract the title and description using Requests-HTML and format it a bit
	# title = response.html.find('h1', first=True).text
	# description = response.html.find('.description', first=True)
	# description = '\n\n'.join(description.text.splitlines()[:-1])

 #   # And template it
	# return render_template(
 #       'response.txt',
 #       title=title,
 #       description=description,
 #       url=response.url


 #   )

def Weather_expression(parameters):

	print(parameters)
	date=parameters.get('date','Today')
	city=parameters.get('geo-city','Delhi')
	api_key = "f328045491f04c9a180dc792630f59a2"
	base_url = "http://api.openweathermap.org/data/2.5/weather?"
	# print(city)
	
	complete_url = base_url + "appid=" + api_key + "&q=" + city
	response = requests.get(complete_url) 
  

	x = response.json() 
 
	if x["cod"] != "404":
		y = x["main"]
		current_temperature = y["temp"]-273
		current_pressure = y["pressure"]
		current_humidiy = y["humidity"]

		z = x["weather"] 
		weather_description = z[0]["description"] 
		currentTemp=str(current_temperature)
		pressure=str(current_pressure)
		humidity=str(current_humidiy) 
		description=str(weather_description) 

		weather_desc = "Temperature is {} with atmospheric pressure {} and humidity in air is {} and description {}".format(currentTemp,pressure,humidity,description)
    	
		return city,weather_desc
  
	else: 
		return "City Not Found"




# translator = Translator()
# translator.translate('안녕하세요.', dest='ja')
# translator.translate('veritas lux mea', src='english')
# translator.translate('안녕하세요.', dest='ja')
# translator.translate('veritas lux mea', src='la')

# translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
# for translation in translations:
# 	print(translation.origin, ' -> ', translation.text)

def tranlator_description(parameters):

		print(parameters)
		word = parameters.get('any')
		language = parameters.get('language','en')

		if(language.lower()=='english'):
			langcode = 'en'
		elif(language.lower()=='hindi'):
			langcode = 'hi'
		elif(language.lower()=='chinese'):
			langcode = 'ja'
		else:
			langcode='en'

		data=translator.translate(word,dest=langcode)
		print(data)
		return word,data.text



def get_news(parameters):
	client.topic = parameters.get('News_type')
	client.language = parameters.get('language', '')
	client.location = parameters.get('geo-country', '')
	return client.get_news()

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg,session_id):
	response = detect_intent_from_text(msg,session_id)
	print(response)
	if (response.intent.display_name == 'show_news_details'):
		news = get_news(dict(response.parameters))
		news_str = 'Here is your news : '
		for row in news :
			news_str+="\n\n{}\n\n{}\n\n".format(row['title'],row['link'])
		return news_str[:500]

	elif (response.intent.display_name == 'Weather_Details'):
		report = dict(response.parameters)
		word,expression=Weather_expression(report)
		return '{}:{}:'.format(word,expression)

	elif (response.intent.display_name == 'language_translator'):
		report = dict(response.parameters)
		word,expression=tranlator_description(report)
		return '{}:{}:'.format(word,expression)

		#return "ok,i will show you news {}",format(dict(response.parameters))
	else:
		return response.fulfillment_text
		# return response.fulfilment_text,"text"