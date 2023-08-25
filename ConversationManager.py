import json
from Chatbot import Chatbot


class ConversationManager:
    def __init__(self):
        with open("personalities.json") as personality_file:
            personalities = json.load(personality_file)

        self.available_personalities = list(personalities.keys())
        if len(self.available_personalities) > 1:
            print('With whom would you like to cht today?')
            for i, personality in enumerate(self.available_personalities):
                print(f'[{i}] {personality}')

    def select_personality(self, personality_index: int):
        try:
            return Chatbot(self.available_personalities[personality_index])
        except IndexError:
            print('Invalid personality index, please try again')
            return None


if __name__ == "__main__":
    conversation_manager = ConversationManager()
    selected_personality = None
    while not selected_personality:
        user_input = input("User: ")
        selected_personality = conversation_manager.select_personality(int(user_input))



    while True:
        user_input = input("User: ")

        response = selected_personality.generate_response(user_input)
        if response == "See you next time":
            break

        print(f"{selected_personality.name}: {response}")
