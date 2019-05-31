import json
from botocore.vendored import requests

TELE_TOKEN='' # put your token here
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)
SCRYFALL_FUZZY = "https://api.scryfall.com/cards/named?fuzzy=" 

def lambda_handler(event, context):
    message = json.loads(event['body'])
    chat_id = message['message']['chat']['id']
    reply = message['message']['text']
    scryfall_search(reply, chat_id)
    return {
        'statusCode': 200
    }
    
def scryfall_search(text, chat_id):
    bot_name = '/search'
    response = ""
    if text.find(bot_name) == 0:
        text = text[7:]
        final_text = SCRYFALL_FUZZY + text
        r = requests.get(final_text)
        object = r.json()
        if object['object'] == "card":
            card = object['image_uris']['normal']
            response = card
        elif object['code'] == "not_found" and "type" in object:
            response = "Too many cards match ambiguous name"
        elif object['code'] == "not_found":
            response = "Card not found"
        else:
            response = "Oops, somthing has gone horribly wrong!"
        return_scryfall(response, chat_id)
        
def return_scryfall(response, chat_id):
        url = URL + "sendMessage?text={}&chat_id={}".format(response, chat_id)
requests.get(url)
