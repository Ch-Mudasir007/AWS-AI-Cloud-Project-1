import json
#first lambda function
def lambda_handler(event, context):
    # Log the incoming event for debugging purposes
    print("Event from Lex:", json.dumps(event, indent=2))

    # Extract session state and intent information
    session_state = event.get('sessionState', {})
    intent = session_state.get('intent', {})
    slots = intent.get('slots', {})
    intent_name = intent.get('name')

    # Retrieve the slot values, handle if they're None
    pizzatype = slots.get('pizzatype', {}).get('value', {}).get('interpretedValue') if slots.get('pizzatype') else None
    pizzasize = slots.get('pizzasize', {}).get('value', {}).get('interpretedValue') if slots.get('pizzasize') else None
    crusttype = slots.get('crusttype', {}).get('value', {}).get('interpretedValue') if slots.get('crusttype') else None
    toppings = slots.get('toppings', {}).get('value', {}).get('interpretedValue') if slots.get('toppings') else None
    customer_name = slots.get('Customer-Name', {}).get('value', {}).get('interpretedValue') if slots.get('Customer-Name') else None
    contact_info = slots.get('Contact-Info', {}).get('value', {}).get('interpretedValue') if slots.get('Contact-Info') else None
    order_time = slots.get('Order-Time', {}).get('value', {}).get('interpretedValue') if slots.get('Order-Time') else None

    # Print slot values for debugging
    print(f"Pizza Type: {pizzatype}, Size: {pizzasize}, Crust: {crusttype}, Toppings: {toppings}")
    print(f"Customer Name: {customer_name}, Contact Info: {contact_info}, Order Time: {order_time}")

    # Check for missing slots and elicit the next required slot
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
    
    # If the order time is missing or not recognized, ask again
    elif order_time is None:
        return elicit_slot(intent_name, slots, 'Order-Time', "When would you like your pizza to be delivered or ready for pickup? You can say something like '5 PM' or 'tomorrow at noon'.")

    # If all slots are filled, confirm and close the conversation
    return close_order(intent_name, slots, f"Thank you {customer_name}! Your {pizzasize} {pizzatype} pizza with {crusttype} crust and {toppings} will be ready at {order_time}. We'll contact you at {contact_info}.")

# Function to elicit the next slot
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

# Function to close the conversation after all slots are filled
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
                "state": "Fulfilled"  # Ensuring intent state is fulfilled
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }
