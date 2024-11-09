import json
import boto3
from datetime import datetime

# AWS clients
comprehend = boto3.client('comprehend')
polly_client = boto3.client('polly')
s3_client = boto3.client('s3')

S3_BUCKET_NAME = 'cs-chatbot-ordering-pizza'

def lambda_handler(event, context):
    # Log the entire incoming event for debugging
    print("Incoming event from Lex:", json.dumps(event, indent=2))

    # Retrieve session state and intent information safely
    session_state = event.get('sessionState', {})
    intent = session_state.get('intent', {})
    intent_name = intent.get('name', 'UnknownIntent')
    slots = intent.get('slots', {})

    # Print intent and slot details
    print(f"Current Intent: {intent_name}")
    print(f"Slots received: {json.dumps(slots, indent=2) if slots else 'No slots received'}")

    # Check for NoneType to avoid AttributeError and handle gracefully
    if slots is None or not isinstance(slots, dict):
        print("Warning: No slots found in the incoming event.")
        return simple_response("I'm here to help you order a pizza or answer questions about our menu.", intent)

    # Extract slot values if available
    pizzatype = get_slot_value(slots, 'pizzatype')
    pizzasize = get_slot_value(slots, 'pizzasize')
    crusttype = get_slot_value(slots, 'crusttype')
    toppings = get_slot_value(slots, 'toppings')
    customer_name = get_slot_value(slots, 'Customer-Name')
    contact_info = get_slot_value(slots, 'Contact-Info')
    order_time = get_slot_value(slots, 'Order-Time')

    # Check the intent and handle accordingly
    if intent_name == "GreetIntent":
        print("Handling GreetIntent...")
        return simple_response("Welcome, to Pizza House! How may I help you?", intent)

    elif intent_name == "OrderingPizza":
        print("Handling OrderingPizza intent...")

        # Use input transcript for sentiment analysis if provided
        user_input = event.get("inputTranscript", "")
        sentiment = None
        if user_input:
            sentiment = analyze_sentiment(user_input)
            print(f"Sentiment detected from user input: {sentiment}")

        # Temporarily hard-code sentiment to test response
        sentiment = "NEGATIVE"  # Hard-coded to "NEGATIVE" to verify response handling

        # Elicit missing slot
        missing_slot = check_missing_slots(slots)
        if missing_slot:
            print(f"Eliciting slot: {missing_slot}")
            return elicit_slot(intent_name, slots, missing_slot, f"Could you please provide the {missing_slot}?")

        # Finalize and confirm order if all slots are filled
        message = create_order_message(pizzasize, pizzatype, crusttype, toppings, customer_name, order_time, contact_info, sentiment)

        # Try generating audio; fall back if it fails
        audio_url = None
        try:
            audio_url = generate_speech_and_upload(message, f"order_confirmation_{customer_name}")
        except Exception as e:
            print(f"Polly or S3 error: {e}")

        return close_order(intent_name, slots, message, audio_url)

    else:
        print("Intent not recognized or triggering fallback response.")
        return simple_response("I'm here to help you order a pizza or answer questions about our menu.", intent)

def get_slot_value(slots, slot_name):
    # Safely retrieve slot value with robust None checking
    if slots is None:
        print(f"Warning: Slots object is None when trying to retrieve '{slot_name}'.")
        return None
    slot = slots.get(slot_name)
    if not slot or not isinstance(slot, dict):
        print(f"Warning: Slot '{slot_name}' is missing or not in expected format.")
        return None
    value = slot.get('value', {}).get('interpretedValue')
    print(f"Retrieved {slot_name}: {value}")
    return value

def check_missing_slots(slots):
    required_slots = ["pizzatype", "pizzasize", "crusttype", "toppings", "Customer-Name", "Contact-Info", "Order-Time"]
    for slot in required_slots:
        if not get_slot_value(slots, slot):
            return slot
    return None

def analyze_sentiment(text):
    try:
        response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        sentiment = response['Sentiment']
        print(f"Comprehend Sentiment Analysis Result: {sentiment}")  # Log to capture sentiment result
    except Exception as e:
        print(f"Sentiment analysis failed: {e}")
        sentiment = "UNKNOWN"  # Use "UNKNOWN" to identify failures
    return sentiment

# Generates order confirmation message
def create_order_message(pizzasize, pizzatype, crusttype, toppings, customer_name, order_time, contact_info, sentiment):
    # Debug logs to check values at this point
    print(f"Creating order message with sentiment: {sentiment}")
    if sentiment == 'NEGATIVE':
        return (f"Thank you {customer_name}. Sorry you're not feeling great. "
                f"Enjoy your {pizzasize} {pizzatype} pizza with {crusttype} crust and {toppings}!")
    return (f"Thank you {customer_name}! Your {pizzasize} {pizzatype} pizza with {crusttype} crust and "
            f"{toppings} will be ready at {order_time}. Contact: {contact_info}.")

def generate_speech_and_upload(text, filename):
    response = polly_client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    audio_stream = response['AudioStream'].read()
    
    filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=f"orders/{filename}", Body=audio_stream, ContentType='audio/mpeg')
    
    audio_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/orders/{filename}"
    print(f"Audio URL generated: {audio_url}")
    return audio_url

def simple_response(message, intent):
    print(f"Sending simple response: {message}")
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled"
            },
            "intent": intent
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }

def elicit_slot(intent_name, slots, slot_to_elicit, message):
    print(f"Eliciting slot {slot_to_elicit} with message: {message}")
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

def close_order(intent_name, slots, message, audio_url):
    print("Finalizing order and closing dialog.")
    messages = [{"contentType": "PlainText", "content": message}]
    if audio_url:
        messages.append({"contentType": "PlainText", "content": f"You can listen to your order confirmation here: {audio_url}"})
    
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
        "messages": messages
    }
