import os
import json
import random
import requests
from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
from db import FileDatabase
from twilio.rest import Client
import pyttsx3

# Initialize the text-to-speech engine
# engine = pyttsx3.init()

# Get the details of the current voice
# voice = engine.getProperty("voice")


# Set the speaking rate to 150 words per minute
# engine.setProperty("rate", 150)

# Run the event loop to make sure the speech is played
# engine.runAndWait()

account_sid = '[AccountSID]'
auth_token = '[AuthToken]'
client = Client(account_sid, auth_token)

rapid_api_key = '[Your Rapid API Key]'

# Load your OpenAI API key
OpenAI.api_key = "[Open AI API Key]"
db = FileDatabase("database.json")

# or from environment variable:
# OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are a seasoned supermarket salesperson with over 15 years of expertise in helping customers find the best products and providing exceptional service. Your goal is to assist customers in their shopping needs, whether it's suggesting the best items they're looking for or offering related alternatives if the specific item is unavailable.

Your role includes the following tasks:

Item Recommendations: When a customer asks for a specific product, use your extensive knowledge to recommend the best options available in the store. If the exact item is not in stock, suggest similar alternatives that meet the customer's requirements.

Engage and Assist: Be courteous and attentive to customers' inquiries. Engage in friendly conversations and ask clarifying questions to better understand their preferences and needs.

Order Placement: If the customer expresses interest in buying a recommended item, offer to place the order for them. Ask for their delivery address and phone number to ensure a smooth delivery process.

Order Confirmation: After collecting the necessary information, confirm the order and provide the customer with a confirmation message, assuring them that their order is processed and will be delivered to the provided address.

Your responses should be polite, helpful, and professional throughout the interaction. Remember to prioritize customer satisfaction and make their shopping experience as convenient as possible.
"""


def getSimilarProducts(product):
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    querystring = {"query": product,"page":"1","country":"US","category_id":"aps"}
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    productsData = data["data"]['products']
    return productsData

@bot()
def on_message(message_history: List[Message], state: dict = None):
    productTypeFunction = [
        {
            "name": "get_product_details",
            "description": "Get Product Details",
            "parameters": {
                "type": "object",
                "properties": {
                    "product client wants to buy": {
                        "type": "string",
                        "description": "product client is interested in buying",
                    },
                    "address of client": {
                        "type": "string",
                        "description": "address of client",
                    },
                    "contact of client": {
                        "type": "string",
                        "description": "phone contact of client",
                    },
                    
                },
            },
        }
    ]

    response = OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
        model="gpt-3.5-turbo",
        functions=productTypeFunction,
        function_call="auto"
    )
    
    
    finish_reason = response["choices"][0]["finish_reason"]
    bot_response = "some error occured. Try again later"
    print(response)
    if finish_reason == "stop":
        bot_response = response["choices"][0]["message"]["content"]
    elif finish_reason == "function_call":
        data = json.loads(response["choices"][0]["message"]["function_call"]["arguments"])
        if data.get('product client wants to buy') is not None and data.get('address of client') is None and data.get('address of client') is None :
            print("CALLED 1")
            searchProduct = data["product client wants to buy"]
            findProductsInDB = db.find(searchProduct)
            productsDataInDB = findProductsInDB['Data']
            productsDataInDBLength = len(productsDataInDB)
            if productsDataInDBLength == 5:
                random_number = random.randint(0, productsDataInDBLength - 1) 
                bot_response = findProductsInDB['Data'][random_number]
            else :    
                products = getSimilarProducts(searchProduct)
                productsResponse = "Great Pick! Here are some products you'd like \n\n"
                for index,product in enumerate(products):
                    if index < 5:
                        productsResponse += ("\n \n"
                                            +"No. " + str(index + 1) 
                                            +  " " +  product["product_title"] 
                                            +"\n \n" 
                                            +"Link : " + product['product_url'] 
                                            +"\n \n" 
                                            +"Price : " + product['product_price']
                                            +"\n \n\r\t\v") 
                    else :
                        break
                db.add({'ID' : searchProduct , 'Data' : [productsResponse] })
                bot_response =  productsResponse
        elif data.get("contact of client") is not None and data.get("address of client") is not None and data.get("contact of client") is not None:
            message = client.messages.create(
              from_='whatsapp:+14155238886',
              body='Thank you for ordering. Your order will be delivered soon.',
              to='whatsapp:+91' + data["contact of client"] 
            )
            print(message.sid)
            bot_response =  "Thank you for ordering! We have placed your order. You will a confirmation message on your whatsapp shortly!"
            
        

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
            "state": state
        },
        "errors": [
            {
                "message": ""
            }
        ]
    }

    return {
        "status_code": 200,
        "response": response
    }
