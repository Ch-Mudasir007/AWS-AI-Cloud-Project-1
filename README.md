# Pizza Ordering Chatbot with Sentiment Analysis

This repository contains the code for a **Pizza Ordering Chatbot** built using **Amazon Lex** and **AWS Lambda**. The chatbot helps users place pizza orders, guiding them through selecting their desired pizza type, size, crust, and other details. Additionally, the chatbot integrates **Amazon Comprehend** to analyze the sentiment of user input, offering an enhanced and empathetic conversational experience.

## Project Overview

The **Pizza Ordering Chatbot** allows users to interact with a virtual assistant for ordering pizza. The chatbot collects necessary information from users, such as pizza type, size, crust, toppings, and contact details. It intelligently prompts users for missing information and confirms the order when all slots are filled.

The chatbot utilizes **sentiment analysis** to adjust its responses based on the user's emotional tone, providing a more personalized and empathetic experience.

### Key Features

- **Pizza Order Collection**: Collects essential details from the user, including pizza type, size, crust, toppings, and contact info.
- **Slot Elicitation**: Uses Amazon Lex's dialog management to prompt users for missing details.
- **Order Confirmation**: Once all details are provided, the chatbot confirms the order in a friendly summary.
- **Sentiment Analysis**: Analyzes the user’s sentiment (positive, negative, or neutral) using Amazon Comprehend and adjusts responses accordingly.
  - **Positive sentiment**: Friendly and enthusiastic responses.
  - **Negative sentiment**: More empathetic and supportive tone to uplift the user’s mood.

## Services and Technologies Used

This project makes use of several AWS services to provide a smooth, automated, and intelligent user experience:

1. **Amazon Lex**: A service for building conversational interfaces. It processes user inputs and manages the flow of the conversation.
2. **AWS Lambda**: A serverless compute service that runs the chatbot’s backend logic, including processing user input, collecting order details, and calling Amazon Comprehend for sentiment analysis.
3. **Amazon Comprehend**: A natural language processing (NLP) service used to analyze the sentiment of the user’s input and modify the chatbot's response based on whether the sentiment is positive, negative, or neutral.

## Advantages of This Approach

1. **Enhanced User Experience**:
   - Sentiment analysis allows the chatbot to respond in a way that matches the user's emotional state, making the interaction feel more human and empathetic.
   - Users with negative sentiments, such as frustration or stress, receive more thoughtful, supportive responses.

2. **Automated Pizza Ordering**:
   - The chatbot guides users through the pizza ordering process automatically, ensuring all required information is collected before confirming the order.
   - This reduces the likelihood of errors in orders and ensures smooth communication with the customer.

3. **Scalability**:
   - Using AWS Lambda and Amazon Lex allows the solution to scale easily, handling multiple users simultaneously without additional infrastructure management.
   - The serverless architecture ensures cost-efficiency by only charging for actual usage.

4. **Adaptability**:
   - The chatbot can easily be extended to other scenarios or integrated with other systems, such as payment gateways or order management systems.
   - Sentiment analysis can be further enhanced to recognize additional emotions (e.g., anger, surprise) for even more personalized responses.

5. **Cost-Effective**:
   - The use of serverless AWS services such as Lambda, Lex, and Comprehend ensures minimal upfront costs and pay-as-you-go pricing, which is ideal for small to medium-sized businesses.

## Workflow

1. **User Input**: The user initiates a conversation with the chatbot by providing details about their pizza order (e.g., type, size, crust).
2. **Slot Filling**: The chatbot collects all the necessary details. If any information is missing, it prompts the user for the required data.
3. **Sentiment Analysis**: During the conversation, the sentiment of the user’s input is analyzed. The chatbot adjusts its responses based on whether the sentiment is positive or negative.
4. **Order Confirmation**: Once all slots are filled, the chatbot confirms the pizza order, including a summary of the details, and thanks the user.
5. **End Conversation**: The chatbot closes the conversation once the order is confirmed.

## Future Enhancements

- **Voice Integration**: Integrate **Amazon Polly** to convert chatbot text responses to speech, allowing users to interact with the chatbot through voice commands.
- **Image Upload**: Allow users to upload pictures of pizzas for recommendations or to place custom orders.
- **Reordering**: Enable users to quickly reorder past pizzas by storing order history.
- **Multilingual Support**: Extend sentiment analysis and conversation capabilities to multiple languages.

## Conclusion

This project demonstrates the power of AWS services in building an intelligent, empathetic pizza ordering chatbot. By integrating **Amazon Lex**, **AWS Lambda**, and **Amazon Comprehend**, we have created a system that not only facilitates easy and efficient pizza ordering but also adapts to the user’s emotional tone. This project can be further extended to enhance user interactions and support additional use cases.

## Getting Started

To deploy and use this pizza ordering chatbot, follow the instructions in the repository's setup guide. Ensure you have the necessary AWS services configured and the appropriate IAM roles set up for accessing Amazon Comprehend and Amazon Lex.
