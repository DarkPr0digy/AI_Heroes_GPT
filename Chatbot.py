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

        # Test
        self.api_key = config["api_keys"]["open_ai"]

        openai.api_key = self.api_key

    def generate_response(self, user_input: str):
        raise NotImplementedError("Subclasses must implement this method.")

    def get_start_message(self):
        return self.introduction


if __name__ == "__main__":
    chatbot = Chatbot(name="CovidBot", introduction="I am a chatbot")
