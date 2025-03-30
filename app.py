from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply
from pymongo import MongoClient
import datetime
# from twilio.rest import Client
# # from weather import Weather, Unit


# cclient = Client()

# from_whatsapp_number='+917838383227'
# to


client = MongoClient("mongodb+srv://gunjan:gunjan@cluster0-tcyic.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('users_bot_db')
records = db.users_bot_records

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World! Updated newwww message"

@app.route("/sms", methods=['POST']) #request coming from twilio
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message



    print(request.form)
    msg = request.form.get('Body')
    sender = request.form.get('From')



# records.count_documents({})

    new_user = { 'sender':sender,'message_body':msg,'sender_id':sender,'send_at' : str(datetime.datetime.now())}
    records.insert_one(new_user)

    # print(condition.text)

    # Create reply
    resp = MessagingResponse()  
    # reply,reply_type = fetch_reply(msg,sender)

    # if reply_type == 'text'
    # resp.message(reply)
    #  return(str)

    resp.message("You said: {}".format(msg)).media("https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png")
    resp.message(fetch_reply(msg,sender))
    return str(resp)




if __name__ == "__main__":
    app.run(debug=True)
