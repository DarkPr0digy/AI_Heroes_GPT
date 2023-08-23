import requests
import json
import openai


class Chatbot:
    def __init__(self, name: str, introduction: str):
        self.name = name
        self.introduction = introduction

        # GPT API Key
        with open("config.json") as config_file:
            config = json.load(config_file)

        self.api_key = config["api_keys"]["open_ai"]
        openai.api_key = self.api_key

        self.messages = []

    def generate_response(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})

        conversation = openai.ChatCompletion.create(
            model="gpt-3.5",
            messages=self.messages,
            temperature=0.9)

        response = conversation.choices[0].message.content

        self.messages.append({"role": self.name, "content": response})

        return response

    def get_start_message(self):
        return self.introduction


if __name__ == "__main__":
    chatbot = Chatbot(name="CovidBot", introduction="I am a chatbot")
