import json
import re
import boto3  # Import boto3 for AWS SDK

# Initialize Comprehend client
comprehend = boto3.client('comprehend')

# Lambda function
def lambda_handler(event, context):
    print("Event from Lex:", json.dumps(event, indent=2))

    session_state = event.get('sessionState', {})
    intent = session_state.get('intent', {})
    slots = intent.get('slots', {})
    intent_name = intent.get('name')

    pizzatype = slots.get('pizzatype', {}).get('value', {}).get('interpretedValue') if slots.get('pizzatype') else None
    pizzasize = slots.get('pizzasize', {}).get('value', {}).get('interpretedValue') if slots.get('pizzasize') else None
    crusttype = slots.get('crusttype', {}).get('value', {}).get('interpretedValue') if slots.get('crusttype') else None
    toppings = slots.get('toppings', {}).get('value', {}).get('interpretedValue') if slots.get('toppings') else None
    customer_name = slots.get('Customer-Name', {}).get('value', {}).get('interpretedValue') if slots.get('Customer-Name') else None
    contact_info = slots.get('Contact-Info', {}).get('value', {}).get('interpretedValue') if slots.get('Contact-Info') else None
    order_time = slots.get('Order-Time', {}).get('value', {}).get('interpretedValue') if slots.get('Order-Time') else None

    print(f"Pizza Type: {pizzatype}, Size: {pizzasize}, Crust: {crusttype}, Toppings: {toppings}")
    print(f"Customer Name: {customer_name}, Contact Info: {contact_info}, Order Time: {order_time}")

    # Call Amazon Comprehend for sentiment analysis
    if customer_name:
        sentiment = analyze_sentiment(customer_name)
        print(f"Detected Sentiment: {sentiment}")

    # Elicit slots based on missing inputs
    if pizzatype is None:
        return elicit_slot(intent_name, slots, 'pizzatype', "What type of pizza would you like?")
    elif pizzasize is None:
        return elicit_slot(intent_name, slots, 'pizzasize', "What size pizza would you like? (Small, Medium, Large)")
    elif crusttype is None:
        return elicit_slot(intent_name, slots, 'crusttype', "What type of crust would you like?")
    elif toppings is None:
        return elicit_slot(intent_name, slots, 'toppings', "What toppings would you like?")
    elif customer_name is None:
        return elicit_slot(intent_name, slots, 'Customer-Name', "Can I have your name, please?")
    elif contact_info is None:
        return elicit_slot(intent_name, slots, 'Contact-Info', "Please provide your contact information.")
    elif order_time is None:
        return elicit_slot(intent_name, slots, 'Order-Time', "When would you like your pizza to be delivered or ready for pickup?")

    # Generate a final response based on sentiment
    if sentiment == 'NEGATIVE':
        message = f"Thank you {customer_name}. I'm sorry to hear you might not be feeling great. We hope our {pizzasize} {pizzatype} pizza with {crusttype} crust and {toppings} will cheer you up!"
    else:
        message = f"Thank you {customer_name}! Your {pizzasize} {pizzatype} pizza with {crusttype} crust and {toppings} will be ready at {order_time}. We'll contact you at {contact_info}."

    return close_order(intent_name, slots, message)

# Function to analyze sentiment using Comprehend
def analyze_sentiment(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']

# Elicit slot function
def elicit_slot(intent_name, slots, slot_to_elicit, message):
    return {
        "sessionState": {
            "dialogAction": {
                "slotToElicit": slot_to_elicit,
                "type": "ElicitSlot"
            },
            "intent": {
                "name": intent_name,
                "slots": slots,
                "state": "InProgress"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }

# Close order function
def close_order(intent_name, slots, message):
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled"
            },
            "intent": {
                "name": intent_name,
                "slots": slots,
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }
