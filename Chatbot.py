import json
import openai
import os
from datetime import datetime


class Chatbot:
    def __init__(self, name: str):
        """ Create a chatbot with a given personality
        :param name: Name of the personality
        """

        self.name = name
        self.introduction = None
        self.characteristic = None

        self.user_total_characters = 0
        self.chatbot_total_words = 0

        # Load API Key from Config File
        with open("config.json") as config_file:
            config = json.load(config_file)

        self.api_key = config["api_keys"]["open_ai"]
        openai.api_key = self.api_key

        self.messages = []

        # Load Personality and Introduce Chatbot
        self._load_personality(name)
        self._introduce()

    def _load_personality(self, personality_name: str):
        """ Load the personality from the personalities.json file
        :param personality_name: Name of the personality
        """

        with open("personalities.json") as personality_file:
            personalities = json.load(personality_file)

        personality_data = personalities.get(personality_name)

        if personality_data:
            self.introduction = personalities[personality_name]["starting_message"]
            self.characteristic = personalities[personality_name]["characteristic"]
        else:
            raise ValueError(f"Personality {personality_name} not found")

    def _introduce(self):
        """ Introduce the chatbot to the user
        """
        self.messages.extend([{"role": "system", "content": self.characteristic},
                              {"role": "assistant", "content": self.introduction}])
        print(f"{self.name}: {self.introduction}")

    def generate_response(self, user_input: str):
        """ Generate a response to the user input
        :param user_input: Input from the user
        :return: Response from the chatbot"""

        if user_input.lower() == "exit":
            self._conversational_insights()
            return "See you next time"

        self.messages.append({"role": "user", "content": user_input})

        conversation = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.9)

        response = conversation.choices[0].message.content

        self.messages.append({"role": "assistant", "content": response})

        # Update Counts
        self.user_total_characters += len(user_input)
        self.chatbot_total_words += len(response.split(" "))

        return response

    def _conversational_insights(self):
        """ Generate conversational insights and save them to a file
        """
        self.messages.append(
            {"role": "system", "content": "Generate a python formatted dictionary containing the topic of our "
                                          "conversation based on the users input, and if it cannot be determined return UNKNOWN, with its key being 'topic'. Additionally, the name of the user if it can "
                                          "be determined, if not return UNKNOWN, with its key being 'user_name'. Send only the dictionary as a string."})

        conversation = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.9)

        # Try get response and convert to dictionary
        response = conversation.choices[0].message.content
        # response = eval(response)

        try:
            response_dict = json.loads(response)
            print(response_dict)
            topic = response_dict.get('topic')
            user_name = response_dict.get('user_name')
        except:
            topic = "UNKNOWN"
            user_name = "UNKNOWN"


        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        conversation_meta_information = {
            "Name of chatbot": self.name,
            "Number of characters typed by user": self.user_total_characters,
            "Number of words used by chatbot": self.chatbot_total_words,
            "Subject of conversation": topic,
            "Name of user": user_name}

        conversation_data = {
            "meta-data": conversation_meta_information,
            "messages": self.messages[1:len(self.messages)-1]}

        if not os.path.exists('./conversations'):
            os.makedirs('conversations')

        filename = f'conversations/conversation_{timestamp}.json'

        with open(filename, 'w') as file:
            json.dump(conversation_data, file, indent=4)

