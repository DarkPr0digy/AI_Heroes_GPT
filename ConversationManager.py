import json
from datetime import datetime
import os
from Chatbot import Chatbot


class ConversationManager:
    """A class to manage conversations and personality selection"""
    def __init__(self):
        """
        Create a conversation manager instance
        """
        # Determine Available Chatbots
        with open("personalities.json") as personality_file:
            personalities = json.load(personality_file)

        self.available_personalities = list(personalities.keys())

        # Determine Available Conversations
        self.available_conversations = os.listdir('conversations')

    def select_personality(self):
        """Select a personality to chat with
        :return: Chatbot instance of the selected personality
        """
        print('With whom would you like to chat today?')
        for i, personality in enumerate(self.available_personalities):
            print(f'[{i}] {personality}')

        selected_personality = None
        while not selected_personality:
            user_input = input("User: ")
            selected_personality = self._create_personality(user_input)

        return selected_personality

    def _create_personality(self, personality_index):
        """Used to create a personality instance to chat with based on the index
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

    def select_conversation(self):
        """Select a conversation to chat with
        :return: Chatbot instance of the selected conversation
        """
        conversation_files = os.listdir('conversations')

        for i, filename in enumerate(conversation_files):
            # Create a datetime object from the filename
            date = datetime.strptime(filename.split('_')[1].rstrip('.json'), "%Y%m%d-%H%M%S")
            date = date.strftime("%d %B %Y at %H:%M:%S")

            with open(os.path.join('conversations', filename)) as conversation_file:
                conversation = json.load(conversation_file)
                chatbot_name = conversation['meta-data']['Name of chatbot']
                chat_topic = conversation['meta-data']['Subject of conversation']

            print(f'[{i}] Conversation with {chatbot_name} about {chat_topic} on the {date}')

        recreated_chatbot = None

        while not recreated_chatbot:
            user_input = input("User: ")
            recreated_chatbot = self._recreate_personality(user_input)

        # Delete Former Conversation - New one will be created
        os.remove(os.path.join('conversations', conversation_files[int(user_input)]))

        return recreated_chatbot

    def _recreate_personality(self, conversation_index):
        """Used to recreate a personality instance to chat with based on the index
        :param conversation_index: Index of the conversation to chat with
        :return: Chatbot instance of the selected conversation
        """
        try:
            conversation_file = self.available_conversations[int(conversation_index)]
            with open(os.path.join('conversations', conversation_file)) as file:
                conversation = json.load(file)
                chatbot_name = conversation['meta-data']['Name of chatbot']
                total_words = conversation['meta-data']['Number of words used by chatbot']
                total_characters = conversation['meta-data']['Number of characters typed by user']
                messages = conversation['messages']

            return Chatbot(chatbot_name, total_words, total_characters, messages)
        except IndexError:
            print('Invalid conversation index, please try again')
            return None
        except ValueError:
            print('Conversation must be entered as an int, please try again')
            return None


if __name__ == "__main__":
    conversation_manager = ConversationManager()

    print("What would you want to do?")
    print("[0] continue a conversation")
    print("[1] start a new conversation")

    decision = -1
    while decision not in [0, 1]:
        try:
            decision = int(input("User: "))
            if decision not in [0, 1]:
                print("Please enter a valid number (0 or 1)")
        except ValueError:
            print("Please enter a number")

    if decision == 0:
        selected_personality = conversation_manager.select_conversation()
    else:
        selected_personality = conversation_manager.select_personality()

    while True:
        user_input = input("User: ")

        response = selected_personality.generate_response(user_input)
        if response == "See you next time":
            break

        print(f"{selected_personality.name}: {response}")
