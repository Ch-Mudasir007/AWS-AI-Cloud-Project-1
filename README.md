# Pizza Ordering Chatbot - Lambda Function

This document provides an overview of the AWS Lambda function designed for a pizza ordering chatbot integrated with Amazon Lex and Amazon Comprehend. The function processes user inputs, manages conversation flow, confirms orders, and adapts responses based on sentiment analysis.

## Overview

The Lambda function is responsible for:

- Collecting user inputs for a pizza order.
- Eliciting any missing information from the user.
- Confirming the order once all necessary details are provided.
- Performing sentiment analysis using Amazon Comprehend to adjust responses based on user emotions.

## Code Structure

### 1. Lambda Handler Function

- **Function Name**: `lambda_handler(event, context)`
- **Purpose**: Entry point for the Lambda function to process incoming events from Amazon Lex.
- **Parameters**:
  - `event`: The input data from Amazon Lex, containing user interactions.
  - `context`: Runtime information for the Lambda function (not used in this implementation).
  
#### Key Steps in the Handler
1. **Log the incoming event** for debugging purposes.
2. **Extract session state, intent, and slots** from the event.
3. **Retrieve values for various slots** (pizza type, size, crust, toppings, etc.) and handle cases where slots may not be provided.
4. **Print slot values** for debugging.
5. **Check for missing slots** and prompt the user for specific information using the `elicit_slot` function.
6. **Sentiment Analysis**:
   - Use Amazon Comprehend to analyze the sentiment of the user's message (positive or negative).
   - Adjust the conversation flow or response based on the sentiment. For example:
     - If the sentiment is **negative**, the bot may offer a more empathetic or supportive response.
     - If the sentiment is **positive**, the bot proceeds with the order as usual.
   
### 2. Slot Elicitation

- **Function Name**: `elicit_slot(intent_name, slots, slot_to_elicit, message)`
- **Purpose**: Prompt the user for a specific slot that is missing.
- **Parameters**:
  - `intent_name`: The name of the intent being processed.
  - `slots`: The current state of all slots.
  - `slot_to_elicit`: The specific slot that needs to be filled.
  - `message`: The prompt message to ask the user.
  
- **Return Value**: Returns a JSON object that specifies the dialog action to elicit the missing slot.

### 3. Closing the Order

- **Function Name**: `close_order(intent_name, slots, message)`
- **Purpose**: Confirm the order once all required information has been gathered.
- **Parameters**:
  - `intent_name`: The name of the intent being processed.
  - `slots`: The final state of all slots.
  - `message`: The confirmation message to send to the user.
  
- **Return Value**: Returns a JSON object indicating that the conversation can be closed, with a fulfillment state.

### 4. Sentiment Analysis with Amazon Comprehend

- **Function Name**: `analyze_sentiment(text)`
- **Purpose**: Analyze the sentiment of the user input using Amazon Comprehend.
- **Parameters**:
  - `text`: The user's input text that needs sentiment analysis.
  
- **Return Value**: Returns the sentiment (positive, negative, or neutral) detected in the input message.
  
- **Usage in Lambda Handler**: The sentiment is used to tailor the bot’s response. Based on the sentiment analysis:
  - **Positive Sentiment**: The chatbot continues with a friendly, upbeat conversation flow.
  - **Negative Sentiment**: The chatbot adjusts its tone to be more empathetic and supportive.

#### Example Integration:
```python
# Function to analyze sentiment using Amazon Comprehend
def analyze_sentiment(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    return sentiment
