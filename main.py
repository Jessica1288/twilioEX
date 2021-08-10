import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import json
import requests

app = Flask('app')

weather_id = os.environ['weather_app_id']

news_id = os.environ['news_app_id']

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("testing!")

    return str(resp)


# weather API
@app.route('/weather', methods=['GET', 'POST'])
def weather():
  city = request.values['Body']

  response = requests.get('http://api.openweathermap.org/data/2.5/weather', params={
    'appid': weather_id,
    'units': 'metric',
    'q': city
  })

  data = json.loads(response.content)
  temp = data['main']['temp']


  return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>{}-{}</Message>
  </Response>""".format(city, temp)



# News API
@app.route('/news', methods=['GET', 'POST'])
def news():
  keyword = request.values['Body']

  response = requests.get('https://newsapi.org/v2/everything', params={
    'q': keyword,
    'sortBy':'popularity',
    'apiKey': news_id
  })

  data = json.loads(response.content)
  article = ""
  message = ""
  if data['totalResults'] > 0:
    article = data['articles'][0]
    message = "Here's the most popular article for {}".format(keyword)
  else:
    message = "There's no article for {}".format(keyword)

  return """<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Message>For {},{}</Message>
  </Response>""".format(message, article)
    


app.run(debug=True, host='0.0.0.0', port = 8080)
#if __name__ == "__main__":
 #   app.run(debug=True)
