import json
from Chatbot import Chatbot


class Vera(Chatbot):
    def __init__(self):
        # Get Introductory Message and Characteristics
        with open("personalities.json") as intro_file:
            config = json.load(intro_file)

        intro_message = config["starting_message"]["vera"]
        characteristic = config["characteristic"]["vera"]

        super().__init__(name="Vera", introduction=intro_message)

        self.messages.extend([{"role": "system", "content": characteristic},
                             {"role": "assistant", "content": intro_message}])


if __name__ == "__main__":
    chatbot = Vera()

    print(f"{chatbot.name}: {chatbot.get_start_message()}")

    while True:
        user_input = input("User: ")

        response = chatbot.generate_response(user_input)

        print(f"{chatbot.name}: {response}")

