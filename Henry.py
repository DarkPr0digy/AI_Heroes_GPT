from Chatbot import Chatbot


class Henry(Chatbot):
    def __init__(self):
        super().__init__(name="Henry")
        self.load_personality("Henry")
        self.introduce()


if __name__ == "__main__":
    chatbot = Henry()

    while True:
        user_input = input("User: ")

        response = chatbot.generate_response(user_input)
        print(f"{chatbot.name}: {response}")
