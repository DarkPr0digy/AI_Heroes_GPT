import json
from Chatbot import Chatbot


class ConversationManager:
    """A class to manage conversations and personality selection"""
    def __init__(self):
        """
        Create a conversation manager instance
        """
        # Determine Personality User Wants to Chat With
        with open("personalities.json") as personality_file:
            personalities = json.load(personality_file)

        self.available_personalities = list(personalities.keys())
        print('With whom would you like to chat today?')
        for i, personality in enumerate(self.available_personalities):
            print(f'[{i}] {personality}')

    def select_personality(self, personality_index):
        """Select a personality to chat with based on the index
        :param personality_index: Index of the personality to chat with
        :return: Chatbot instance of the selected personality
        """
        try:
            return Chatbot(self.available_personalities[int(personality_index)])
        except IndexError:
            print('Invalid personality index, please try again')
            return None
        except ValueError:
            print('Personalities must be entered as an int, please try again')
            return None


if __name__ == "__main__":
    conversation_manager = ConversationManager()
    selected_personality = None
    while not selected_personality:
        user_input = input("User: ")
        selected_personality = conversation_manager.select_personality(user_input)

    while True:
        user_input = input("User: ")

        response = selected_personality.generate_response(user_input)
        if response == "See you next time":
            break

        print(f"{selected_personality.name}: {response}")
