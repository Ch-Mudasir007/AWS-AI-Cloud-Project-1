import json
import boto3  # Import boto3 for AWS SDK

# Lambda function
def lambda_handler(event, context):
    print("Event from Lex:", json.dumps(event, indent=2))

    session_state = event.get('sessionState', {})
    intent = session_state.get('intent', {})
    slots = intent.get('slots', {})
    intent_name = intent.get('name')

    pizzatype = get_slot_value(slots, 'pizzatype')
    pizzasize = get_slot_value(slots, 'pizzasize')
    crusttype = get_slot_value(slots, 'crusttype')
    toppings = get_slot_value(slots, 'toppings')
    customer_name = get_slot_value(slots, 'Customer-Name')
    contact_info = get_slot_value(slots, 'Contact-Info')
    order_time = get_slot_value(slots, 'Order-Time')

    print(f"Pizza Type: {pizzatype}, Size: {pizzasize}, Crust: {crusttype}, Toppings: {toppings}")
    print(f"Customer Name: {customer_name}, Contact Info: {contact_info}, Order Time: {order_time}")

    # Elicit slots based on missing inputs or invalid inputs
    if not pizzatype or pizzatype not in ["Veg", "Non-Veg"]:
        return elicit_slot(intent_name, slots, 'pizzatype', "Please choose a valid pizza type (Veg or Non-Veg).")
    
    if not pizzasize or pizzasize not in ["Small", "Medium", "Large", "Extra-Large", "Party Size"]:
        return elicit_slot(intent_name, slots, 'pizzasize', "Please choose a valid pizza size (Small, Medium, Large, Extra-Large, Party Size).")
    
    if not crusttype or crusttype not in ["Thin", "Thick", "Cheese-Stuffed"]:
        return elicit_slot(intent_name, slots, 'crusttype', "Please choose a valid crust type (Thin, Thick, Cheese-Stuffed).")
    
    if not toppings:
        return elicit_slot(intent_name, slots, 'toppings', "Please provide toppings for your pizza (e.g., cheese, olives, mushrooms, etc.).")
    
    if not customer_name:
        return elicit_slot(intent_name, slots, 'Customer-Name', "Can I have your name, please?")
    
    if not contact_info:
        return elicit_slot(intent_name, slots, 'Contact-Info', "Please provide your contact information.")
    
    if not order_time:
        return elicit_slot(intent_name, slots, 'Order-Time', "When would you like your pizza to be delivered or ready for pickup?")

    # Generate a response based on the user inputs
    message = f"Thank you {customer_name}! Your {pizzasize} {pizzatype} pizza with {crusttype} crust and {toppings} will be ready at {order_time}. We'll contact you at {contact_info}."
    
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