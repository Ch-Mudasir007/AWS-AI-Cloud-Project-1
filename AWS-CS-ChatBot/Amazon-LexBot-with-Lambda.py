import json
import re
from datetime import datetime

# Function to resolve time into 24-hour format
def resolve_time(input_time):
    # Check if the input time is in 12-hour format (e.g., 4PM or 4AM)
    if re.match(r'\d{1,2}(AM|PM)', input_time, re.IGNORECASE):
        # Convert 12-hour format to 24-hour format
        time_obj = datetime.strptime(input_time, "%I%p")
        return time_obj.strftime("%H:%M")  # 24-hour format
    else:
        # If already in 24-hour format (e.g., 16:00), return as is
        return input_time

# Lambda function
def lambda_handler(event, context):
    print("Event from Lex:", json.dumps(event, indent=2))

    session_state = event.get('sessionState', {})
    intent = session_state.get('intent', {})
    slots = intent.get('slots', {})
    intent_name = intent.get('name')
    session_attributes = event.get('sessionState', {}).get('sessionAttributes', {})

    pizzatype = get_slot_value(slots, 'pizzatype')
    pizzasize = get_slot_value(slots, 'pizzasize')
    crusttype = get_slot_value(slots, 'crusttype')
    toppings = get_slot_value(slots, 'toppings')
    customer_name = get_slot_value(slots, 'Customer-Name')
    contact_info = get_slot_value(slots, 'Contact-Info')
    order_time = get_slot_value(slots, 'Order-Time')

    # Elicit slots if inputs are missing or invalid
    if not pizzatype or pizzatype not in ["Veg", "Non-Veg"]:
        return elicit_slot(intent_name, slots, 'pizzatype', "Please choose a valid pizza type (Veg or Non-Veg).")
    
    if not pizzasize or pizzasize not in ["Small", "Medium", "Large", "Extra-Large", "Party Size"]:
        return elicit_slot(intent_name, slots, 'pizzasize', "Please choose a valid pizza size (Small, Medium, Large, Extra-Large, Party Size).")
    
    if not crusttype or crusttype not in ["Thin", "Thick", "Cheese-Stuffed"]:
        return elicit_slot(intent_name, slots, 'crusttype', "Please choose a valid crust type (Thin, Thick, Cheese-Stuffed).")
    
    # Check toppings input against the allowed list and allow multiple toppings
    if not toppings:
        return elicit_slot(intent_name, slots, 'toppings', "Please provide valid toppings from the list: cheese, olives, mushrooms, pepperoni, onions, peppers, pineapple, bacon.")
    
    toppings_list = [topping.strip().lower() for topping in toppings.split(',')]
    allowed_toppings = ["cheese", "olives", "mushrooms", "pepperoni", "onions", "peppers", "pineapple", "bacon"]
    
    # Validate each topping
    invalid_toppings = [topping for topping in toppings_list if topping not in allowed_toppings]
    
    if invalid_toppings:
        return elicit_slot(intent_name, slots, 'toppings', f"Invalid toppings: {', '.join(invalid_toppings)}. Please choose from: {', '.join(allowed_toppings)}.")
    
    if not customer_name:
        return elicit_slot(intent_name, slots, 'Customer-Name', "Can I have your name, please?")
    
    if not contact_info:
        return elicit_slot(intent_name, slots, 'Contact-Info', "Please provide your contact information.")
    
    if not order_time:
        return elicit_slot(intent_name, slots, 'Order-Time', "When would you like your pizza to be delivered or ready for pickup?")

    # Resolve order time to 24-hour format
    order_time_24hr = resolve_time(order_time)

    # Join toppings back into a string for display
    toppings_display = ', '.join([topping.capitalize() for topping in toppings_list])

    # Generate response without sentiment message
    message = f"Thank you {customer_name}! Your {pizzasize} {pizzatype} pizza with {crusttype} crust and {toppings_display} will be ready at {order_time_24hr}. We'll contact you at {contact_info}. Enjoy your pizza!"
    
    return close_order(intent_name, slots, message)

# Function to get the slot value safely
def get_slot_value(slots, slot_name):
    return slots.get(slot_name, {}).get('value', {}).get('interpretedValue', '').strip() if slots.get(slot_name) else None

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
            },
            "sessionAttributes": {}
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
            },
            "sessionAttributes": {}
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }
