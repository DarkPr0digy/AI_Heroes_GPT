import json
import openai
import os
from datetime import datetime


class Chatbot:
    def __init__(self, name: str):
        self.name = name
        self.introduction = None
        self.characteristic = None

        # GPT API Key
        with open("config.json") as config_file:
            config = json.load(config_file)

        self.api_key = config["api_keys"]["open_ai"]
        openai.api_key = self.api_key

        self.messages = []

        self._load_personality(name)
        self._introduce()

    def _load_personality(self, personality_name: str):
        with open("personalities.json") as personality_file:
            personalities = json.load(personality_file)

        personality_data = personalities.get(personality_name)

        if personality_data:
            self.introduction = personalities[personality_name]["starting_message"]
            self.characteristic = personalities[personality_name]["characteristic"]
        else:
            raise ValueError(f"Personality {personality_name} not found")

    def _introduce(self):
        self.messages.extend([{"role": "system", "content": self.characteristic},
                              {"role": "assistant", "content": self.introduction}])
        print(f"{self.name}: {self.introduction}")

    def generate_response(self, user_input: str):
        if user_input.lower() == "exit":
            return "See you next time"

        self.messages.append({"role": "user", "content": user_input})

        conversation = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.9)

        response = conversation.choices[0].message.content

        self.messages.append({"role": "assistant", "content": response})

        return response
