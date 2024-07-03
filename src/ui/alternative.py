import json
from typing import Any

import gradio as gr
import time

import requests

CHAT_HISTORY = []
LOCAL_LLM_URL = "http://host.docker.internal:1234/v1"
COMPLETE_URL = f"{LOCAL_LLM_URL}/chat/completions"


class ChatProcessor:
    def __init__(self):
        self.chat_history = CHAT_HISTORY

    def llm_predict(self, msg: str, chatbot: Any, submit: bool):
        """
        Generator which yields response for the chatbox widget. The forma of response is a list of lists with inner list
        of length 2 where first element is a user query and second is a chat bot response. Each new iteration adds words
         to the response
        """
        print(msg)
        print(chatbot)
        print(submit)

        self.chat_history.append([msg, ""])
        # Yield the chat history with new user query before sending request to the LLM but make sure to do it one time for iteration
        print("Return empty chat history before sending request to LLM")

        # Convert chat history to an LLM format
        llm_chat_history = [
            # SYSTEM MESSAGE
            {"role": "system", "content": "Always answer in rhymes."},
        ]
        for messages in self.chat_history:
            llm_chat_history.append({"role": "user", "content": messages[0]})
            if messages[1]:
                llm_chat_history.append({"role": "assistant", "content": messages[1]})

        # Send streaming request to the local LLM server
        payload = {
            "model": "mistral-7b-instruct-v0.1.Q2_K",
            "messages": llm_chat_history,
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": True,
        }
        print("Sending request to LLM server:")
        response = requests.post(COMPLETE_URL, json=payload, stream=True)
        response.raise_for_status()
        print("Response from LLM server:")
        for line in response.iter_lines():
            if line:
                print(line)
                line = line.decode('utf-8')
                if not line.startswith("data:"):
                    print("Skipping non-data line")
                    continue

                json_line = line[6:].strip()

                if json_line == "[DONE]":
                    break

                data = json.loads(json_line)
                print(data)
                # Append the response to the chat history
                if not 'content' in data['choices'][0]["delta"]:
                    print("Skipping empty response")
                    continue

                # Append the response to the chat history
                self.chat_history[-1][1] += data['choices'][0]["delta"]['content']
                yield "", self.chat_history


with gr.Blocks() as demo:
    chat = ChatProcessor()

    chatbot = gr.Chatbot(value=chat.chat_history, placeholder="Start chatting with the bot!")
    msg = gr.Textbox()
    submit = gr.Button("Submit")
    clear = gr.ClearButton()

    submit.click(chat.llm_predict, [msg, chatbot, submit], [msg, chatbot])


