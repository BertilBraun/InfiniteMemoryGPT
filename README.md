# Infinite Memory Chatbot

This project is a chatbot that combines the OpenAI GPT API and Vector Databases such as Milvus and Pinecone to create a chatbot that can remember conversations and use them to generate responses.

## Idea

The main Idea is to have a Database that stores all the conversations that the chatbot has had. Then, when the chatbot is asked a question, it will search the database for all the conversations that are similar to the question. These conversations will then be injected into the Prompt that is sent to the OpenAI API. The API will then generate a response based on the Prompt and the chatbot will send the response to the user. This allows the chatbot to always have knowledge of the relevant conversations that it has had in the past.

## Usage

To use the chatbot, you must first create a config.json file in the root directory of the project. Refer to config.example.json for an example of the config file.
There are multiple ways to use the chatbot. You can find examples in chat.py, answer.py and many utility functions in util.util.py.
